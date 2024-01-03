# -*- coding: UTF-8 -*-

import json
import os
import time

import requests
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from sse_starlette import EventSourceResponse
from loggers import logger
from webserver_utils import WebResponseJson
from as_constants import AS_HOME_DIR, YUAN_2_URL

app = FastAPI()

app.mount("/yuan-chat", StaticFiles(directory=os.path.join(AS_HOME_DIR, "dist")), name="dist")
templates = Jinja2Templates(directory=os.path.join(AS_HOME_DIR, "dist"))

CHAT_INFER_ERROR_MESSAGE = "你好，源大模型推理失败了，请重试！"


@app.get("/")
def home(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request
        }
    )


@app.get("/hello")
def world(request: Request):
    return {"world"}


class ChatSseSubscribeRequestInfo(BaseModel):
    messages: list = []
    response_length: int = 5000
    temperature: float = 0.6
    top_p: float = 0.95
    top_k: int = 0


@app.post('/sse/subscribe')
def stream(item: ChatSseSubscribeRequestInfo):
    # define stream
    def event_stream(msg: list, res_len: int, temperature: float, top_p: float, top_k: int):
        try:
            if len(msg) <= 0:
                logger.info("event_stream error, len(msg) <= 0, msg:" + msg)
                res_msg_dict = get_result_message(CHAT_INFER_ERROR_MESSAGE, int(time.time() * 1000))
                yield json.dumps(get_result_dict(True, "", "", res_msg_dict))
                return

            # get result
            response_text = get_infer_result(msg, 0, res_len, temperature, top_p, top_k)
            res_msg_dict = get_result_message(response_text, int(time.time() * 1000))
            yield json.dumps(get_result_dict(True, "", "", res_msg_dict))
        except Exception as ex:
            logger.error("event_stream error, message:%s; ex:%s", msg, str(ex))
            res_msg_dict = get_result_message(CHAT_INFER_ERROR_MESSAGE, int(time.time() * 1000))
            yield json.dumps(get_result_dict(True, "", "", res_msg_dict))
    return EventSourceResponse(event_stream(item.messages, item.response_length,
                                            item.temperature, item.top_p, item.top_k))


# result
def get_result_dict(flag: bool, err_code: "", err_msg: "", res_data: None):
    return {"flag": flag, "errCode": err_code, "errMessage": err_msg, "resData": res_data}


# infer result
def get_result_message(message: str, create_time: time):
    return {"message": message, "time": create_time}


def get_infer_result(message: [], intent: int, response_len: int, temperature: float, top_p: float, top_k: int):
    multi_dialogue = False
    if len(message) > 1:
        multi_dialogue = True
    chat_infer_request_param = {"input": message, "url": YUAN_2_URL, "style": intent, "multidialogue": multi_dialogue,
                                "response_length": response_len, "temperature": temperature, "top_p": top_p,
                                "top_k": top_k}
    try:
        response = WebResponseJson()
        res = response.modelsYuanInfer(chat_infer_request_param)
        if not res.get("flag"):
            logger.info("get_infer_result res.flag not true, errmsg:" + res.get("errMessage"))
            return res.get("errMessage")
        else:
            res_data = res.get("resData")
            out_put = res_data.get("output")
            sorted(out_put, key=lambda x: x["score"], reverse=False)
            return out_put[0].get("content")
    except Exception as ex:
        logger.error("message:%s;Exception:%s", message, str(ex))
        return CHAT_INFER_ERROR_MESSAGE


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5050)
    