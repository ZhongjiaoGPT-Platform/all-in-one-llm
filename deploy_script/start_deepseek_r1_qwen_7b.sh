#!/bin/bash

source ~/.zshrc
conda activate vllm-infer
unset http_proxy
unset https_proxy

CUDA_VISIBLE_DEVICES=3 vllm serve /models/llm/deepseek-ai/DeepSeek-R1-Distill-Qwen-7B \
--served-model-name ZhongjiaoGPT/Qwen \
--host 0.0.0.0 \
--port 8012 \
--gpu-memory-utilization 1 \
--max-model-len 100000 \
--enable-auto-tool-choice \
--tool-call-parser hermes \
--chat-template /models/llm/Qwen/template.jinja

