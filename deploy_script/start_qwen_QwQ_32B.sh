#!/bin/bash

source ~/.zshrc
conda activate vllm-infer
unset http_proxy
unset https_proxy

CUDA_VISIBLE_DEVICES=0,1,2,3 vllm serve /models/llm/Qwen/QwQ-32B-Preview \
--served-model-name ZhongjiaoGPT/Qwen \
--host 0.0.0.0 \
--port 8012 \
--tensor-parallel-size 4 \
--gpu-memory-utilization 1 \
--enable-auto-tool-choice \
--tool-call-parser hermes \
--chat-template /models/llm/Qwen/template.jinja

