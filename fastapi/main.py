import requests
import urllib
import time
import os
from typing import Optional, Union, Annotated

from fastapi import FastAPI, Request, HTTPException, Security, Depends, File, UploadFile
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.responses import Response
from fastapi.staticfiles import StaticFiles

from routers.embed import router as EmbRouter
from routers.vllm import router as VllmRouter
from routers.whisper_cpp import router as WhisperRouter
from schemas import CustomModel, Models, FreeFormJSON


app = FastAPI(title="All In One LLM", version="1.0.1")

llm_1gpu_replicas = int(os.getenv('LLM_1GPU_REPLICAS', '0') or '0')
llm_2gpu_replicas = int(os.getenv('LLM_2GPU_REPLICAS', '0') or '0')
llm_4gpu_replicas = int(os.getenv('LLM_4GPU_REPLICAS', '0') or '0')
llm_8gpu_replicas = int(os.getenv('LLM_8GPU_REPLICAS', '0') or '0')
alm_replicas = int(os.getenv('ALM_REPLICAS', '0') or '0')
code_llm_replicas = int(os.getenv('CODE_LLM_REPLICAS', '0') or '0')
whisper_replicas = int(os.getenv('ASR_REPLICAS', '0') or '0')
vlm_replicas = int(os.getenv('VLM_REPLICAS', '0') or '0')
emb_replicas = int(os.getenv('EMB_REPLICAS', '0') or '0')
qwq_replicas = int(os.getenv('QWQ_REPLICAS', '0') or '0')
deepseek_r1_replicas = int(os.getenv('DeepSeek_R1_REPLICAS', '0') or '0')

remote_emb = int(os.getenv('REMOTE_EMB', '0') or '0')
remote_emb_base = os.getenv('REMOTE_EMB_BASE', '0')

remote_llm = int(os.getenv('REMOTE_LLM', '0') or '0')
remote_llm_base = os.getenv('REMOTE_LLM_BASE', '0')

print("################################")
print("llm_1gpu_replicas", llm_1gpu_replicas)
print("llm_2gpu_replicas", llm_2gpu_replicas)
print("llm_4gpu_replicas", llm_4gpu_replicas)
print("llm_8gpu_replicas", llm_8gpu_replicas)
print("alm_replicas", alm_replicas)
print("code_llm_replicas", code_llm_replicas)
print("whisper_replicas", whisper_replicas)
print("vlm_replicas", vlm_replicas)
print("emb_replicas", emb_replicas)
print("qwq_replicas", qwq_replicas)
print("deepseek_r1_replicas", deepseek_r1_replicas)

print("remote_emb", remote_emb)
print("remote_emb_base", remote_emb_base)
print("remote_llm", remote_llm)
print("remote_llm_base", remote_llm_base)
print("################################")

if llm_1gpu_replicas > 0:
    LLM_URL = "http://llm-qwen2_5-7b:8012"
elif llm_2gpu_replicas > 0:
    LLM_URL = "http://llm-qwen2_5-72b-int4-2gpu:8012"
elif llm_4gpu_replicas > 0:
    LLM_URL = "http://llm-qwen2_5-72b-int4:8012"
elif llm_8gpu_replicas > 0:
    LLM_URL = "http://llm-qwen2_5-72b:8012"
elif code_llm_replicas > 0:
    LLM_URL = "http://llm-qwen2_5-code:8012"
elif qwq_replicas > 0:
    LLM_URL = "http://llm-qwen-qwq-32b:8012"
else:
    LLM_URL = "http://localhost:8012"

if remote_llm > 0:
    LLM_URL = remote_llm_base
    llm_8gpu_replicas = 1

VLM_URL = "http://vlm-qwen2-vl-7b:8022"
EMB_URL = "http://embed-gte-qwen2-7b:8112"
ALM_URL = "http://llm-qwen2-audio-7b:8032"
ASR_URL = "http://whisper-large-v3:8132"
REASON_LLM_URL = "http://deepseek-r1:8072"

if remote_emb > 0:
    EMB_URL = remote_emb_base
    emb_replicas = 1

# auth
auth_scheme = HTTPBearer(scheme_name="API key")
API_KEY = os.getenv("API_KEY")

if not API_KEY:
    def check_api_key():
        pass

else:
    def check_api_key(api_key: Annotated[HTTPAuthorizationCredentials, Depends(auth_scheme)]):
        if api_key.scheme != "Bearer":
            raise HTTPException(status_code=403, detail="Invalid authentication scheme")
        if api_key.credentials != API_KEY:
            raise HTTPException(status_code=403, detail="Invalid API key")

        return api_key.credentials


# image upload dir
UPLOAD_DIRECTORY = "/app/uploaded_files"
os.makedirs(UPLOAD_DIRECTORY, exist_ok=True)
app.mount("/files", StaticFiles(directory=UPLOAD_DIRECTORY), name="files")


@app.post("/upload-file/")
async def upload_file(file: UploadFile = File(...)):
    file_location = os.path.join(UPLOAD_DIRECTORY, file.filename)
    with open(file_location, "wb") as f:
        f.write(await file.read())
    return {"info": f"File '{file.filename}' uploaded successfully.", "url": f"/files/{file.filename}"}


@app.get("/files/{filename}")
async def get_file(filename: str):
    file_path = os.path.join(UPLOAD_DIRECTORY, filename)
    if os.path.exists(file_path):
        return FileResponse(file_path)
    else:
        raise HTTPException(status_code=404, detail="File not found")


@app.get("/health")
def health_check(request: Request, api_key: str = Security(check_api_key)) -> Response:
    """Health check for multiple services based on replica counts."""

    def check_service_health(url: str) -> bool:
        """Helper function to check the health of a service."""
        try:
            response = requests.get(f"{url}/health", timeout=5)
            return response.status_code == 200
        except requests.RequestException:
            return False

    def check_service_accessible(url: str) -> bool:
        """Check if a service is accessible (ping/curl-like logic)."""
        try:
            response = requests.get(url, timeout=5)
            return response.status_code in {200, 403}  # Assuming accessible if it responds
        except requests.RequestException:
            return False

    # Map services to their replica counts and URLs
    services = {
        "LLM": {
            "replicas": llm_1gpu_replicas + llm_2gpu_replicas +  llm_4gpu_replicas + llm_8gpu_replicas + code_llm_replicas + qwq_replicas,
            "url": LLM_URL,
            "check_health": True,
        },
        "REASON_LLM": {"replicas": deepseek_r1_replicas, "url": REASON_LLM_URL, "check_health": True},
        "VLM": {"replicas": vlm_replicas, "url": VLM_URL, "check_health": True},
        "EMB": {"replicas": emb_replicas, "url": EMB_URL, "check_health": True},
        "ALM": {"replicas": alm_replicas, "url": ALM_URL, "check_health": True},
        "ASR": {"replicas": whisper_replicas, "url": ASR_URL, "check_health": False},  # Check accessibility only
    }

    # Check health or accessibility for each service with replicas > 0
    for service, info in services.items():
        if info["replicas"] > 0:
            if info["check_health"]:
                # Perform health check
                if not check_service_health(info["url"]):
                    return Response(status_code=500)
            else:
                # Perform accessibility check for ASR
                if not check_service_accessible(info["url"]):
                    return Response(status_code=500)

    # All required services are healthy
    return Response(status_code=200)


@app.get("/v1/models/{model}", tags=["OpenAI"])
@app.get("/v1/models", tags=["OpenAI"])
def get_models(
    request: Request, model: Optional[str] = None, api_key: str = Security(check_api_key)
) -> Union[Models, CustomModel]:
    """
    Show available models
    """
    def fetch_model_info(url: str, headers: Optional[dict], model_type: str, owner: str, created: Optional[int] = None) -> dict:
        """Fetch and format model information from a service."""
        try:
            response = requests.get(url, headers=headers).json()
            return {
                "id": response["data"][0]["id"],
                "object": "model",
                "owned_by": owner,
                "created": created or response["data"][0]["created"],
                "type": model_type,
            }
        except Exception:
            return None

    headers = {"Authorization": f"Bearer {api_key}"} if api_key else None

    # Initialize models dynamically based on replicas
    models = []

    if llm_1gpu_replicas + llm_2gpu_replicas + llm_4gpu_replicas + llm_8gpu_replicas + code_llm_replicas + qwq_replicas + deepseek_r1_replicas > 0:
        llm_model_data = fetch_model_info(f"{LLM_URL}/v1/models", headers, "text-generation", "vllm")
        if llm_model_data:
            models.append(llm_model_data)

    if deepseek_r1_replicas > 0:
        llm_model_data = fetch_model_info(f"{REASON_LLM_URL}/v1/models", headers, "text-generation", "vllm")
        if llm_model_data:
            models.append(llm_model_data)

    if vlm_replicas > 0:
        vlm_model_data = fetch_model_info(f"{VLM_URL}/v1/models", headers, "image-text-inference", "vllm")
        if vlm_model_data:
            models.append(vlm_model_data)

    if emb_replicas > 0:
        emb_model_data = fetch_model_info(f"{EMB_URL}/v1/models", headers, "text-embeddings-inference", "sglang", created=round(time.time()))
        if emb_model_data:
            models.append(emb_model_data)

    if alm_replicas > 0:
        alm_model_data = fetch_model_info(f"{ALM_URL}/v1/models", headers, "audio-text-inference", "vllm")
        if alm_model_data:
            models.append(alm_model_data)

    if whisper_replicas > 0:
        asr_model_data = {
            "id": "whisper",
            "object": "model",
            "owned_by": "whisper.cpp",
            "created": round(time.time()),
            "type": "audio-text-inference",
        }
        models.append(asr_model_data)

    # If a specific model is requested
    if model is not None:
        # Support double encoding for model ID with "/" character
        model = urllib.parse.unquote(urllib.parse.unquote(model))
        for model_data in models:
            if model == model_data["id"]:
                return model_data
        raise HTTPException(status_code=404, detail="Model not found")

    # Return all available models
    return {"object": "list", "data": models}


@app.post("/v1/embeddings", tags=["OpenAI"])
def embeddings(request: FreeFormJSON):
    pass


@app.post("/v1/completions", tags=["OpenAI"])
def completions(request: FreeFormJSON):
    pass


@app.post("/v1/chat/completions", tags=["OpenAI"])
def chat_completions(request: FreeFormJSON):
    pass

# routers
app.include_router(VllmRouter)
app.include_router(EmbRouter)
app.include_router(WhisperRouter)


