#!/bin/bash

source ~/.zshrc
conda activate vllm-infer
unset http_proxy
unset https_proxy

CUDA_VISIBLE_DEVICES=1 vllm serve /models/llm/Qwen/Qwen2___5-7B-Instruct \
--host 0.0.0.0 \
--port 8012 \
--served-model-name ZhongjiaoGPT/Qwen \
--enable-auto-tool-choice \
--tool-call-parser hermes \
--chat-template /models/llm/Qwen/template.jinja

