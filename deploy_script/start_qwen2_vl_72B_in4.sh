
#!/bin/bash

source ~/.zshrc
conda activate vllm-infer
unset http_proxy
unset https_proxy

CUDA_VISIBLE_DEVICES=0,1,2,3 vllm serve /models/vlm/qwen/Qwen2-VL-72B-Instruct-GPTQ-Int4 \
--served-model-name Qwen/Qwen2-VL-72B-Instruct-GPTQ-Int4 \
--pipeline-parallel-size 4 \
--host 0.0.0.0 \
--port 8023 \
--gpu-memory-utilization 0.95 \
--max-model-len 4096

