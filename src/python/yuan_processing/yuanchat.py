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
CHAT_INFER_PARAM_INVALID = "你好，传递的参数不合法，请确认！"

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
    browser_flag: bool = False
    retrieve_topk: int = 3
    template: str = ""
    access_key: str = ""
    embeddings_model_path: str = ""


@app.post('/sse/subscribe')
def stream(item: ChatSseSubscribeRequestInfo):
    # define stream
    def event_stream(msg: list, res_len: int, temperature: float, top_p: float, top_k: int, browser_flag: bool,
                     retrieve_topk: int, template: str, access_key: str, embedding_path: str):
        try:
            if len(msg) <= 0:
                logger.info("event_stream error, len(msg) <= 0, msg:" + msg)
                res_msg_dict = get_result_info(CHAT_INFER_ERROR_MESSAGE, [], [], browser_flag, int(time.time() * 1000))
                yield json.dumps(get_result_dict(True, "", "", res_msg_dict))
                return

            if browser_flag:
                if not embedding_path or not access_key or not os.path.exists(embedding_path) \
                        or retrieve_topk > 8 or retrieve_topk < 1:
                    res_msg_dict = get_result_info(CHAT_INFER_PARAM_INVALID, [], [], browser_flag, int(time.time() * 1000))
                    yield json.dumps(get_result_dict(True, "", "", res_msg_dict))
                    return

            # get result
            res_msg_dict = get_infer_result(msg, 0, res_len, temperature, top_p, top_k, browser_flag, retrieve_topk,
                                            template, access_key, embedding_path)
            yield json.dumps(get_result_dict(True, "", "", res_msg_dict))
        except Exception as ex:
            logger.error("event_stream error, message:%s; ex:%s", msg, str(ex))
            res_msg_dict = get_result_info(CHAT_INFER_ERROR_MESSAGE, [], [], browser_flag, int(time.time() * 1000))
            yield json.dumps(get_result_dict(True, "", "", res_msg_dict))
    return EventSourceResponse(event_stream(item.messages, item.response_length, item.temperature, item.top_p,
                                            item.top_k, item.browser_flag, item.retrieve_topk, item.template,
                                            item.access_key, item.embeddings_model_path))


# result
def get_result_dict(flag: bool, err_code: "", err_msg: "", res_data: None):
    return {"flag": flag, "errCode": err_code, "errMessage": err_msg, "resData": res_data}


def get_result_info(message: str, refs: [], peopleAlsoAsk: [], browser_flag: bool, create_time: time):
    return {"message": message, "refs": refs, "peopleAlsoAsk": peopleAlsoAsk, "browser_flag": browser_flag,
            "time": create_time}


def get_infer_result(message: [], intent: int, response_len: int, temperature: float, top_p: float, top_k: int,
                     browser_flag: bool, retrieve_topk: int, template: str, access_key: str, embedding_path: str):
    multi_dialogue = False
    if len(message) > 1:
        multi_dialogue = True
    chat_infer_request_param = {"input": message, "url": YUAN_2_URL, "style": intent, "multidialogue": multi_dialogue,
                                "response_length": response_len, "temperature": temperature, "top_p": top_p,
                                "top_k": top_k, "retrieve_topk": retrieve_topk, "template": template,
                                "embeddings_model_path": embedding_path, "serper_api_key": access_key}
    try:
        if not browser_flag:
            response = WebResponseJson()
            res = response.modelsYuanInfer(chat_infer_request_param)
            if not res.get("flag"):
                logger.info("get_infer_result res.flag not true, errmsg:" + res.get("errMessage"))
                return get_result_info(res.get("errMessage"), [], [], False, int(time.time() * 1000))
            else:
                res_data = res.get("resData")
                out_put = res_data.get("output")
                sorted(out_put, key=lambda x: x["score"], reverse=False)
                return get_result_info(out_put[0].get("content"), [], [], False, int(time.time() * 1000))
        else:
            return get_browser_result(chat_infer_request_param)
    except Exception as ex:
        logger.error("message:%s;Exception:%s", message, str(ex))
        return get_result_info(CHAT_INFER_ERROR_MESSAGE, [], [], False, int(time.time() * 1000))


def get_browser_result(chat_infer_request_param):
    try:
        response = WebResponseJson()
        res = response.modelsYuanInfer_web(chat_infer_request_param)
        if not res.get("flag"):
            logger.info("get_infer_web_result res.flag not true, errmsg:" + res.get("errMessage"))
            return get_result_info(res.get("errMessage"), [], [], False, int(time.time() * 1000))
        else:
            res_data = res.get("resData")
            output = res_data.get("output")
            sorted(output, key=lambda x: x["score"], reverse=False)
            content = output[0].get("content")
            refs = output[0].get("refs")
            asks = output[0].get("peopleAlsoAsk")
            source_list = []
            ask_list = []
            for item in refs:
                source = {"url": item["url"], "text": item["text"], "title": item["title"]}
                source_list.append(source)
            for item in asks:
                ask = {"question": item["question"]}
                ask_list.append(ask)
            return get_result_info(content, source_list, ask_list, True, int(time.time() * 1000))
    except Exception as ex:
        logger.error("message:%s;Exception:%s", chat_infer_request_param, str(ex))
        return get_result_info(CHAT_INFER_ERROR_MESSAGE, [], [], False, int(time.time() * 1000))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5050)
    