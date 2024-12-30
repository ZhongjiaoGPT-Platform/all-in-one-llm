
#!/bin/bash

source ~/.zshrc
conda activate vllm-infer
unset http_proxy
unset https_proxy

CUDA_VISIBLE_DEVICES=2,3 vllm serve /models/llm/Qwen/Qwen2___5-Coder-32B-Instruct-AWQ \
--host 0.0.0.0 \
--port 8012 \
--served-model-name ZhongjiaoGPT/Qwen \
--tensor-parallel-size 2 \
--enable-auto-tool-choice \
--tool-call-parser hermes \
--chat-template /models/llm/Qwen/template.jinja

