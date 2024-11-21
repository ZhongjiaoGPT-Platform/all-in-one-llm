FROM python:3.12-slim

WORKDIR /app
ADD ./pyproject.toml ./pyproject.toml

ENV http_proxy=http://10.23.105.143:7890
ENV https_proxy=http://10.23.105.143:7890

RUN mkdir -p ~/.config/pip && \
    echo "[global]" > ~/.config/pip/pip.conf && \
    echo "index-url = https://mirrors.aliyun.com/pypi/simple" >> ~/.config/pip/pip.conf && \
    pip install --upgrade pip && pip install --no-cache-dir .

ADD . .

ENV http_proxy=""
ENV https_proxy=""
