#!/bin/bash

source ~/.zshrc
conda activate vllm-infer
unset http_proxy
unset https_proxy

CUDA_VISIBLE_DEVICES=0,1,2,3 vllm serve /models/vlm/tclf90/qvq-72b-preview-gptq-int4 \
--served-model-name ZhongjiaoGPT/Qwen \
--host 0.0.0.0 \
--port 8022 \
--gpu-memory-utilization 1 \
--max-model-len 32000 \
--tensor-parallel-size 4 \
--enable-auto-tool-choice \
--tool-call-parser hermes \
--chat-template /models/llm/Qwen/template.jinja \
--limit-mm-per-prompt image=24
