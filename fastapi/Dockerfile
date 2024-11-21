FROM python:3.12-slim

WORKDIR /app
ADD ./pyproject.toml ./pyproject.toml

RUN mkdir -p ~/.config/pip && \
    echo "[global]" > ~/.config/pip/pip.conf && \
    echo "index-url = https://mirrors.aliyun.com/pypi/simple" >> ~/.config/pip/pip.conf && \
    pip install --upgrade pip && pip install --no-cache-dir .

ADD . .

