#!/bin/bash

source ~/.zshrc
conda activate vllm-infer
unset http_proxy
unset https_proxy

CUDA_VISIBLE_DEVICES=0,1,2,3 vllm serve /models/llm/Qwen/Qwen2___5-72B-Instruct-GPTQ-Int4 \
--host 0.0.0.0 \
--port 8012 \
--served-model-name ZhongjiaoGPT/Qwen \
--tensor-parallel-size 4

