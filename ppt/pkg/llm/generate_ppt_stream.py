import requests
import ollama
import os
import time
import json
from concurrent.futures import ThreadPoolExecutor
import queue
from pkg.ppt_gen import config

host = config.OLLAMA_SERVER_IP
port = config.OLLAMA_SERVER_PORT
client = ollama.Client(host=f"http://{host}:{port}")

topic = ""
model_list = ["qwen2.5:7b", "gemma2:9b"]

task_q = queue.Queue()

# 设置当前的工作路径
current_work_path = os.path.join(os.getcwd(), "pkg", "template")
print(f"current_work_path: {current_work_path}")
print(f"当前工作目录: {os.getcwd()}")


def cleaned_data(slide_data: str) -> str:
    cleaned_data = slide_data
    for i in range(0, len(slide_data) - 1):
        if slide_data[i] == "{":
            cleaned_data = slide_data[i:]
            break

    for i in range(len(cleaned_data) - 1, -1, -1):
        if cleaned_data[i] == "}":
            cleaned_data = cleaned_data[: i + 1]
            break
    json_dict = cleaned_data
    return json_dict


def generate_outline_from_api(instructions: str, previous_content: str = "", model_id: int = 0):
    """
    method: 生成大纲
    params: instructions:指令,传值为ppt大纲的主题
            previous_content:历史内容json，默认为空，可不传
            model_id:id，默认使用qwen，可不传
    return: 流式返回str
    """
    print(model_list[model_id])
    with open(os.path.join(current_work_path, "generate_outline_template.txt"), "r", encoding="utf-8") as in_file:
        template = in_file.read()
    instructions = instructions
    global topic
    topic = instructions
    print("global topic:", topic)
    previous_content = previous_content
    prompt = f"{template}".format(instructions=instructions, previous_content=previous_content)
    res = client.chat(
        model=model_list[model_id],
        messages=[{"role": "user", "content": prompt}],
        stream=True,
        options={"num_ctx": 32000, "temperature": 0.6, "num_predict": -1},
    )
    # return res["message"]["content"]
    for chunk in res:
        yield chunk["message"]["content"]


def generate_body_stream_from_api(previous_content: str, model_id: int = 0):
    """
    method: 流式生成幻灯片内容
    params: previous_content：历史内容json,不为空
            model_id:id，默认使用qwen，可不传
    return: 循环返回str
    """
    print(model_list[model_id])
    with open(os.path.join(current_work_path, "generate_body_template.txt"), "r", encoding="utf-8") as in_file:
        template = in_file.read()
    previous_content = previous_content
    prompt = f"{template}".format(instructions=topic, previous_content=previous_content)
    res = client.chat(
        model=model_list[model_id],
        messages=[{"role": "user", "content": prompt}],
        stream=True,
        options={"num_ctx": 32000, "temperature": 0.6, "num_predict": -1},
    )
    for chunk in res:
        yield chunk["message"]["content"]


def regenerate_outline_from_api(outline: str, model_id: int = 0):
    """
    method: 重新生成某一章
    params: outline:某一章的json，比如{"heading": heading, "slides": [{"heading": "", "bullet_points": [], "key_message": "", "img_keywords": ""}]}
            model_id:id，默认使用gemma2模型重新生成
    return: 返回str
    """
    print(model_list[model_id])
    with open(os.path.join(current_work_path, "regenerate_outline_template.txt"), "r", encoding="utf-8") as in_file:
        template = in_file.read()
    if isinstance(outline, str):
        outline = json.loads(outline)
    # 清空幻灯片标题，便于生成
    heading = outline["heading"]
    outline = {"heading": heading, "slides": [{"heading": "", "bullet_points": [], "key_message": "", "img_keywords": ""}]}
    global topic
    print("global topic:", topic)
    prompt = f"{template}".format(topic=topic, outline=outline)
    # print("prompt:\n", prompt)
    res = client.chat(
        model=model_list[model_id], messages=[{"role": "user", "content": prompt}], stream=False, options={"num_ctx": 48000, "temperature": 0.5}
    )
    return res["message"]["content"]


def regenerate_body_from_api(body: str, model_id: int = 0):
    """
    method: 重新生成某一张幻灯片
    """
    print(model_list[model_id])
    with open(os.path.join(current_work_path, "regenerate_body_template.txt"), "r", encoding="utf-8") as in_file:
        template = in_file.read()
    if isinstance(body, str):
        body = json.loads(body)
    global topic
    prompt = f"{template}".format(topic=topic, body=body)
    # print(prompt)
    res = client.chat(
        model=model_list[model_id], messages=[{"role": "user", "content": prompt}], stream=False, options={"num_ctx": 32000, "temperature": 0.5}
    )
    return res["message"]["content"]


def generate_each_slide_by_outline(outline: dict, model_id: int = 0):
    """
    method: 根据大纲生成每一页幻灯片。
    params: outline:dict或json类型,大纲内容
            model_id:模型id
    return: body:dict迭代器循环返回每一个幻灯片的生成内容
            i:第i章节
            j:第j张幻灯片
    """
    print(model_list[model_id])
    topic = outline["title"]
    i = 0
    for chapter in outline["chapter"]:
        chapter_topic = topic + " " + chapter["heading"]
        print(chapter_topic)
        j = 0
        for slide in chapter["slides"]:
            with open(os.path.join(current_work_path, "generate_each_slide_template.txt"), "r", encoding="utf-8") as in_file:
                template = in_file.read()
            prompt = f"{template}".format(topic=chapter_topic, body=slide)
            res = client.chat(
                model=model_list[model_id],
                messages=[{"role": "user", "content": prompt}],
                stream=False,
                options={"num_ctx": 4096, "temperature": 0.7, "num_predict": 500},
            )
            content = cleaned_data(res["message"]["content"])  # datahelper中使用的方式返回dict

            try:
                body = json.loads(content)
                # print(content)
            except:
                print("--------------JSON 不合法-----------\n", content)
                content = cleaned_data(fix_json(content))
                try:
                    body = json.loads(content)
                except:
                    body = outline["chapter"][i]["slides"][j]
            finally:
                # print(body, i, j)
                global task_q
                task_q.put([body, i, j])
                # yield body, i, j
            j += 1
        i += 1
    task_q.put("<stop>")
    return


def fix_json(js: str, model_id: int = 0):
    """
    method: 修正有误的字符串。
    params: js:有无的json
            model_id:模型id
    return: str
    """
    print(model_list[model_id])
    try:
        json.loads(js)
        print("当前json不存在问题")
        return js
    except Exception:
        print("当前json存在问题，开始修正")
        prompt = f"""
        请对以下格式有误的JSON字符串进行修正，使其符合标准的JSON格式规范。
        保留原始的JSON结构和内容不变.
        请确保所有键都用双引号括扩起来，所有值的格式都正确（\例如，双引号中的字符串、不带引号的数字、不带引号的布尔值为 true/false），并且存在所有必要的逗号和冒号。
        
        
        ## 存在问题的JSON字符串：
        {js}

        仅输出修正后的JSON字符串。
        ## 输出：
        ```json
        
        """
        res = client.chat(
            model=model_list[model_id], messages=[{"role": "user", "content": prompt}], stream=False, options={"num_ctx": 48000, "temperature": 0.4}
        )
        print("-----------修正后的json-----------\n", res["message"]["content"])
        return res["message"]["content"]


def translate_zn_to_en(zn: str, model_id: int = 0):
    print(model_list[model_id])
    prompt = f"""
    请将下述中文词语或句子翻译为英文的同时扩写一下，用于图生成。
    仅输出一句话。
    ## 中文句子
    {zn}
    
    ## 输出为一句英文
    """
    res = client.chat(
        model=model_list[model_id], messages=[{"role": "user", "content": prompt}], stream=False, options={"num_ctx": 48000, "temperature": 0.4}
    )
    print("翻译为", res["message"]["content"])
    return res["message"]["content"]


if __name__ == "__main__":
    # 测试demo
    model_id = 0
    instructions = [
        "如何理解科技创新赋能新质生产力",
        "“双减”、课间十分钟",
        "中国经济工作将坚持“稳中求进、以进促稳、先立后破”总基调",
        "智能体热潮：人机交互新范式已被大模型打开",
        "围绕中国特色金融文化“五要五不”、行业文化理念、证券行业荣辱观、证券从业人员职业道德准则、公司核心价值观等写一个ppt",
    ]

    # 生成目录
    start_time = time.time()
    result = ""
    for g in generate_outline_from_api(instructions=instructions[0], previous_content="", model_id=model_id):
        result += g
    print(result)
    end_time = time.time()
    print("生成目录时间" + str(end_time - start_time) + "秒")
    previous_content = result

    # # 重写某一章
    # import sys
    # import json

    # sys.path.append(os.path.join(os.getcwd(), "pkg"))
    # from ppt_gen.data_helper import cleaned_slide_data

    # result = ""
    # clean_json = cleaned_slide_data(previous_content)
    # # print(clean_json["chapter"][1])
    # chapter = clean_json["chapter"][1]  # 重写第二章
    # chapter = regenerate_outline_from_api(chapter)
    # clean_json["chapter"][1] = chapter
    # result = clean_json
    # print(result)
    # previous_content = result

    # # 生成正文
    # result = ""
    # start_time = time.time()
    # for g in generate_body_stream_from_api(previous_content=previous_content, model_id=model_id):
    #     result += g
    #     # print(g)
    # print(result)
    # end_time = time.time()
    # print("生成时间" + str(end_time - start_time) + "秒")
    # previous_content = result

    # 生成每一页
    result = ""
    start_time = time.time()
    d_ = json.loads(cleaned_data(previous_content))
    # print(d_["chapter"][0]["slides"][0])
    # for body, i, j in generate_each_slide_by_outline(d_):
    #     d_["chapter"][i]["slides"][j] = body
    # end_time = time.time()
    # print("生成时间" + str(end_time - start_time) + "秒")

    ## 翻译
    # translate_zn_to_en("政策限制严")

    # 线程池测试
    def thread_1():
        global task_q
        while True:
            if not task_q.empty():
                result = task_q.get()
                if isinstance(result, str):
                    print("stop", result)
                    break
                i = result[1]
                j = result[2]
                print(f"当前是第{i+1}章第{j+1}节")

    start_time = time.time()
    thread_pool = ThreadPoolExecutor(max_workers=2)
    task1 = thread_pool.submit(generate_each_slide_by_outline, d_)
    task2 = thread_pool.submit(thread_1)
    while not task2.done():
        continue
        print("-------------运行中-------------")
    end_time = time.time()
    print("线程执行完毕！耗时为：" + str(end_time - start_time))
    thread_pool.shutdown(wait=True)
