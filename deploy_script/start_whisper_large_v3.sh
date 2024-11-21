#!/bin/bash

source ~/.zshrc

unset http_proxy
unset https_proxy

CUDA_VISIBLE_DEVICES=1 /app/server \
	-pc \
	-pr \
	--language zh \
	--prompt "以下是普通话的句子。" \
	-m /models/alm/ggml/ggml-large-v3.bin \
	--host 0.0.0.0 \
	--port 8132


