#!/bin/bash

source ~/.zshrc
conda activate vllm-infer
unset http_proxy
unset https_proxy

CUDA_VISIBLE_DEVICES=3 vllm serve /models/alm/Qwen/Qwen2-Audio-7B-Instruct \
--host 0.0.0.0 \
--port 8032 \
--served-model-name ZhongjiaoGPT/Qwen

