#!/bin/bash

source ~/.zshrc
conda activate vllm-infer
unset http_proxy
unset https_proxy

CUDA_VISIBLE_DEVICES=0,1,2,3 vllm serve /models/llm/deepseek-ai/DeepSeek-R1-Distill-Qwen-32B \
--served-model-name ZhongjiaoGPT/DeepSeek-R1 \
--host 0.0.0.0 \
--port 8072 \
--tensor-parallel-size 4 \
--gpu-memory-utilization 1 \
--max-model-len 100000 \
--enable-reasoning \
--reasoning-parser deepseek_r1 \
--chat-template /models/llm/deepseek-ai/chat_tmpl_r1_think.jinja

