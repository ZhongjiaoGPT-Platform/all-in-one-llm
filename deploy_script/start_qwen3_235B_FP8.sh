#!/usr/bin/env zsh
# set -euxo pipefail

source ~/.zshrc

export RAY_WORKER_NUMBER=1
export GLOO_SOCKET_IFNAME=ens11f0
export TP_SOCKET_IFNAME=ens11f0
export NCCL_SOCKET_IFNAME=ens11f0
export RAY_HEAD_IP=192.168.66.1
export VLLM_HOST_IP=192.168.66.1

# 1️⃣ 等待 Head 健康
echo "等待 Ray Head 健康..."
until ray status --address=$RAY_HEAD_IP:6379 2>/dev/null | grep -q "Active"; do
  sleep 2
done

# 2️⃣ 等待 Worker 加入
TARGET=$((1 + RAY_WORKER_NUMBER))
echo "waiting $TARGET nodes to join (1 Head + $RAY_WORKER_NUMBER Worker)…"
while true; do
  NODE_COUNT=$(ray status --address=$RAY_HEAD_IP:6379 \
    | sed -n '/^Active:/,/^Pending:/p' \
    | grep -c 'node_')
  echo "current NODE_COUNT = $NODE_COUNT"
  if [ "$NODE_COUNT" -ge "$TARGET" ]; then
    echo "found $NODE_COUNT nodes, starting vLLM"
    break
  fi
  sleep 2
done

# 3️⃣ 启动 vLLM 服务（exec 保持容器前台不退出）
echo "启动 vLLM 服务…"
exec vllm serve /root/.cache/huggingface/llm/Qwen/Qwen3-235B-A22B-FP8 \
--host 0.0.0.0 \
--port 8012 \
--served-model-name ZhongjiaoGPT/Qwen \
--tensor-parallel-size 8 \
--pipeline-parallel-size 2 \
--enable-expert-parallel \
--enable-auto-tool-choice \
--tool-call-parser hermes \
--enable-reasoning \
--reasoning-parser qwen3

