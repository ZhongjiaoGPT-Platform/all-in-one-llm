# All in One LLM

![](https://img.shields.io/badge/python-3.10-green) ![](https://img.shields.io/badge/vLLM-v0.6.1.post2-blue) ![](https://img.shields.io/badge/sglang-v0.3.2-red) ![](https://img.shields.io/badge/whisper.cpp-v1.7.1-yellow)

### Deployment a light and full OAI compatible API for production

[vLLM](https://github.com/vllm-project/vllm) is one of the state of the art libraries for deploying a Large Language Model (LLM) and its API with better generation performance. However, based on our own experience, vLLM is not the best way to deploy embedding models and audio models.

Thus this repository adds 1) `/v1/embeddings` endpoint through [SGLang](https://github.com/sgl-project/sglang), 2) audio inference endpoint through [whisper.cpp](https://github.com/ggerganov/whisper.cpp), 3) file upload and access endpoint, 4) automatic switch between LLM and VLM based on user requrest and serves it all on a single port. **The aim of this repository is to have a complete API that's very light, easy to use and maintain !**

**API offer the following OAI type endpoints:**
*  `/v1/models`
*  `/v1/completions`
*  `/v1/chat/completions`
*  `/v1/embeddings`
*  `/inference`
*  `/files`
*  `/upload-file`

## ⚙️ How it works ?

<p align="center">
    <img src="https://github.com/user-attachments/assets/3dd68aca-ba44-4fea-b716-eae9ba7c2914" >
</p>


## 🚀 Quickstart

* First, configure a *.env* file.
  
*  Then, run the containers with Docker compose :

    ```bash
    docker compose --env-file env up --detach
    ```

## 🔦 Usage

check all deployed models:
```bash
curl http://[your host IP]/v1/models
```

check service health:
```bash
curl -v http://[your host IP]/health
```

upload file:
```bash
curl -X POST "http://[your host IP]/upload-file/" -F "file=@[/path/to/your/file]"
```

check uploaded file:
```bash
curl http://[your host IP]/files/test1.jpg
```


To use LLM:
```bash
curl http://[your host IP]/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "Qwen/LLM",
    "messages": [
      {
        "role": "system",
        "content": "You are a helpful assistant."
      },
      {
        "role": "user",
        "content": "Who are you?"
      }
    ]
  }'

curl http://[your host IP]/v1/completions \
  -H "Content-Type: application/json" \
  -d '{
      "model": "Qwen/LLM",
      "prompt": "San Francisco is a",
      "max_tokens": 7,
      "temperature": 0
  }'

curl http://[your host IP]/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "Qwen/LLM",
    "messages": [
      {
        "role": "system",
        "content": "You are a helpful assistant."
      },
      {
        "role": "user",
        "content": "Who are you?"
      }
    ]
  }'

curl http://[your host IP]/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
  "model": "Qwen/LLM",
  "messages": [
    {
      "role": "system",
      "content": "You are a helpful assistant."
    },
    {
      "role": "user",
      "content": "Who won the world series in 2020?"
    },
    {
      "role":
          "assistant",
      "content":
          "The Los Angeles Dodgers won the World Series in 2020."
    },
    {
      "role": "user",
      "content": "Where was it played?"
    }
  ]
}'
```

To use VLM:
```bash
curl -X POST "http://[your host IP]/v1/chat/completions" \
-H "Content-Type: application/json" \
-d '{
    "messages": [{
        "role": "user",
        "content": [{
            "type": "text",
            "text": "whats in the image"
        }, {
            "type": "image_url",
            "image_url": {
                "url": "http://[your host IP]/files/[ur image name]"
            }
        }]
    }],
    "model": "Qwen/VLM",
    "max_tokens": 200,
    "temperature": 0
}'

curl -X POST "http://[your host IP]/v1/chat/completions" \
-H "Content-Type: application/json" \
-d '{
    "messages": [{
        "role": "user",
        "content": [{
            "type": "text",
            "text": "whats in the image"
        }, {
            "type": "image_url",
            "image_url": {
                "url": f"data:image/jpeg;base64,{image_base64}"
            }
        }]
    }],
    "model": "Qwen/VLM",
    "max_tokens": 200,
    "temperature": 0
}'
```

To use Embedding model:
```bash
curl http://[your host IP]/v1/embeddings \
  -H "Content-Type: application/json" \
  -d '{
    "input": "The food was delicious and the waiter...",
    "model": "Qwen/EMB",
    "encoding_format": "float"
  }'
```

To use audio model:
```bash
curl -X POST "http://[your host IP]/v1/chat/completions" \
-H "Content-Type: application/json" \
-d '{
    "messages": [{
        "role": "user",
        "content": [{
            "type": "text",
            "text": "whats in the audio"
        }, {
            "type": "audio_url",
            "audio_url": {
                "url": "http://[your host IP]/files/audio2.wav"
            }
        }]
    }],
    "model": "Qwen/ALM",
    "max_tokens": 200,
    "temperature": 0
}'
```

To use ASR model:
```bash
curl [your host IP]/inference -H "Content-Type: multipart/form-data" -F file="@[path/to/your/wav/file]" -F response_format="json" | jq
```


> Reference: https://github.com/etalab-ia/albert-models/tree/main
