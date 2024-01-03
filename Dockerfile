FROM node:19-alpine AS base
COPY ./src/webui .

RUN npm ci

RUN npm run build

FROM python:3.11-slim as build-image

### install requirements
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

WORKDIR .

COPY . .

COPY --from=base ./dist ./dist

ENV YUAN_2_URL = "http://127.0.0.1:8000/yuan"

ENTRYPOINT  ["/bin/bash", "start.sh"]
