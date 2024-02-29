# -*- coding: utf-8  -*-

import re
import json
import requests
from datetime import datetime
from formula_utils import add_dollor_to_formula
from sensitive_words_filtering import DFAFilter
from loggers import logger
from web_argumnet.fetch_web_content import WebContentFetcher
from web_argumnet.retrieval import EmbeddingRetriever
from web_argumnet.llm_answer import LLMAnswer
from web_argumnet.utils import citation_correction


# 敏感信息过滤
def sensitive_filter():
    gfw = DFAFilter()
    path_list = ['bad-words-adver.txt', 'bad-words-politic.txt', 'bad-words-violence.txt', 'bad-words-porn.txt']
    gfw.parse(path_list)
    return gfw

gfw = sensitive_filter()


# 检验是否不含有标点，不含标点返回True，含有返回False
def isnot_punctuation(strs):
    en_punc = '!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~'
    ch_punc = '＂＃＄％＆＇（）＊＋，－／：；＜＝＞＠［＼］＾＿｀｛｜｝～｟｠｢｣､\u3000、〃〈〉《》「」『』【】〔〕〖〗〘〙〚〛〜〝〞〟〰〾〿–—‘’‛“”„‟…‧﹏﹑﹔·！？｡。'
    allPun = en_punc + ch_punc

    for _char in strs:
        if _char in allPun:
            return False
    return True


# 模型生成
def post_infer_server(ques_id, input_msg, url, paras_dict, timeout=60):
    # 请求传参
    # {
    #     "ques_list":[{"id":"001","ques":"李少是一个缉毒警察，“"}],
    #     "tokens_to_generate":200,
    #     "temperature": 0.6,
    #     "top_p": 0.95,
    #     "top_k": 0,
    # }

    data = {"ques_list": [], "tokens_to_generate": paras_dict['response_length'],
            "temperature": paras_dict["temperature"],
            "top_p": paras_dict['top_p'], "top_k": paras_dict['top_k']}

    for ques in input_msg:
        data["ques_list"].append({"id": ques_id, "ques": ques})

    res = requests.put(url, json=data, timeout=timeout)
    res = json.loads(res.text)
    if res["flag"]:
        response = [id_ans["ans"] for id_ans in res["resData"]["output"]]
        return response
    else:
        raise ValueError("Error happened when call infer-server: "+str(res["exceptionMsg"]))



# 初步处理UI传入文本，包括prompt组合，（输入合法性检验、敏感词检测放在意图识别模块）
def processinput(paras_dict):
    # 输入合法性判断
    assert len(paras_dict["input"])>0, "输入参数input长度必须大于0"
    task_data = paras_dict["input"][-1]["question"].strip()     #获取最新request

    # 对输入request进行合法性检验、敏感词检验
    global gfw
    if task_data == None or task_data == '':
        error_message = "您输入的信息为空，请重新输入"
        return False, error_message
    elif gfw.filter(task_data)[1]:
        error_message = "对不起，您的输入包含敏感信息，请重新输入"
        return False, error_message

    # # 多轮对话判断，paras_dict['multidialogue']==True时，采用多轮对话
    # his_dialogs = []
    # if paras_dict['multidialogue'] and len(paras_dict["input"]) > 1:   #直接使用前几轮对话
    #     his_dialogs = paras_dict["input"][:-1]
    #
    # # 若最后是汉字或字母或数字，加入标点
    # his_dialogs_list = []
    # for QA in his_dialogs:
    #     if len(QA["question"]) > 0 and len(QA["answer"])>0:
    #         QA["question"] = QA["question"].strip()
    #         QA["answer"] = QA["answer"].strip()
    #         if isnot_punctuation(QA["question"][-1]): QA["question"] += "？"
    #         if isnot_punctuation(QA["answer"][-1]): QA["answer"] += "。"
    #         QA["question"] += '<n>'
    #         QA["answer"] += '<n>'
    #         his_dialogs_list.extend([QA["question"], QA["answer"]])

    # # 按照不同style组成输入模型的prompt
    # text = task_data  #若用户输入问题过长，只保留最后的3000字长度
    #
    # # 多轮对话拼接
    # text_kc = ""
    # for i in range(len(his_dialogs_list) - 1, 0, -2):  # (start, end, step), 取值范围[start, end)
    #     text_kc = his_dialogs_list[i - 1] + his_dialogs_list[i] + text_kc  # 必须保证问答的形式存在
    #     if (len(text) + len(text_kc)) > 3000:
    #         text_kc = text_kc[len(his_dialogs_list[i - 1] + his_dialogs_list[i]):]  # 超过字数，将新加入的历史对话去除
    #         break  # 大于1500字不再加入历史对话
    #
    # # 检索信息 + 多轮对话 + 用户输入
    # text = text_kc + text + '<sep>'
    # prompts = [text]

    return True, task_data


# 调用web检索，组成prompt，LLM推理
def infer_server(ques_id, input_query, paras_dict):

    # 基于问题提取网页内容
    web_contents_fetcher = WebContentFetcher(input_query, paras_dict)
    web_contents, serper_response = web_contents_fetcher.fetch()

    if ('serper_response' in serper_response) and ('message' in serper_response['serper_response'])  and serper_response['serper_response']['message'] == 'Unauthorized.':
        raise ValueError("您提供的serper api key不合法，请检查重新输入")
    elif web_contents == []:
        raise ValueError("网络检索结果为空，请检查网络是否通畅")

    #感兴趣相关话题
    if 'peopleAlsoAsk' in serper_response['serper_response']:
        peopleAlsoAsk = serper_response['serper_response']['peopleAlsoAsk']
    elif 'relatedSearches' in serper_response['serper_response']:
        relatedSearches = serper_response['serper_response']['relatedSearches']
        peopleAlsoAsk = [{'question': d['query']} for d in relatedSearches]
    else:
        peopleAlsoAsk = [{'question': input_query}]

    # 基于embeddings检索相关文档
    retriever = EmbeddingRetriever(paras_dict)
    relevant_docs_list = retriever.retrieve_embeddings_noreapt(web_contents, serper_response['links'], input_query)
    content_processor = LLMAnswer(paras_dict)
    formatted_relevant_docs = content_processor._format_reference(relevant_docs_list, serper_response['links'])
    # print(formatted_relevant_docs)
    logger.info('\n ques_id:{0}\t formatted_relevant_docs:{1}'.format(paras_dict["ques_id"], formatted_relevant_docs))

    # # yuan模型获取答案
    ai_message_obj, summary_prompt = content_processor.get_answer_yuan(input_query, formatted_relevant_docs, serper_response['language'], paras_dict)
    answer = ai_message_obj.split('答案：')[-1]
    logger.info('\n\n输入LLM文本：\n:{0}'.format(summary_prompt))
    logger.info('\n ques_id:{0}\t initial_answer:{1}'.format(paras_dict["ques_id"], answer))

    return [answer, peopleAlsoAsk, relevant_docs_list, serper_response]


def clean_str(input_text):
    text = input_text.strip()  # 去除开头结尾\r, \t, \n, 空格等字符
    text = text.replace('<unk>', '').replace('<eod>', '').replace('▃', '\n').replace('▂', ' ').replace('<n>', '\n')

    text = re.sub(r'(\.{6,})', r'......', text)  # 省略号最多6个.
    text = re.sub(r'(。{2,})', r'。', text)  # 两个以上的连续句号只保留一个
    text = re.sub(r'(_{8,})', r'________', text)  # _最多8个.

    return text


# 根据不同的style，调用不同的后处理方式
def postprocess(input_prompts, paras_dict, web_out):
    answer = web_out[0]

    infer_out = [answer]
    result = []
    for res in infer_out:
        res = res.strip()  # 去除开头结尾\r, \t, \n, 空格等字符
        res = clean_str(res)  # 删除特殊字符、表情符
        res, flag = gfw.filter(res)  #将敏感词语用*代替

        # style: 0 代码类别
        check_str = paras_dict["input"][-1]["question"] + res
        check_str_fli = re.sub(r'(python|代码|```|"""|def |int |return |def\(|int\(|return\()', r'', check_str)

        if len(check_str) - len(check_str_fli) > 4:  #若存在两个以上关键词，代码意图
            style = 0
        else:
            style = 1

        if style == 1:
            # 若是公式意图，在公式前后添加$符号
            res = add_dollor_to_formula(res)
        logger.info('\n ques_id:{0}\t intend_recognition:{1}'.format(paras_dict["ques_id"], style))
        # result.append({"content": res.strip(), "typeDesc": "对话", "score": 1})
        result.append(res.strip())

    if len(result) > 0:
        peopleAlsoAsk = web_out[1]
        relevant_docs_list = web_out[2]
        serper_response = web_out[3]

        # 方式二：只选前三的相关参考文档，去重
        refs = []
        for i in range(len(relevant_docs_list)):
            ref = {}
            ref['url'] = (relevant_docs_list[i].metadata)['url']
            ref['text'] = relevant_docs_list[i].page_content

            try:
                ref['title'] = serper_response['titles'][serper_response['links'].index(ref['url'])]
            except:
                ref['title'] = ref['text'].split('。')[0]

            if refs == []:
                refs.append(ref)
            else:
                if ref['url'] == refs[-1]['url'] and ref['text'] != refs[-1]['text']:
                    refs[-1]['text'] += ref['text']
                elif ref['url'] != refs[-1]['url']:
                    refs.append(ref)

        # 引用校正
        answer = citation_correction(result[0], [ref['text'] for ref in refs], paras_dict["embeddings_model_path"])

        output = [{"content": answer.strip(), "refs": refs, "peopleAlsoAsk": peopleAlsoAsk, "typeDesc": "对话", "score": 1}]
    else:
        output = [{"content": "此类问题暂时超出我的回复权限，可以尝试向我提问其他话题。\n我会努力改进自己，为您提供更好的服务，感谢理解。", "refs":"", "peopleAlsoAsk":"", "typeDesc": "对话", "score": 0}]

    return output


# 修改字典所有值，所有str中"用\\"替换
def modify_dict(dictionary):
    for key in dictionary.keys():
        if isinstance(dictionary[key], dict):
            # 如果当前值为字典类型，则进行递归调用
            modify_dict(dictionary[key])
        elif isinstance(dictionary[key], str):
            # 对于非字典类型的值，直接进行修改操作
            dictionary[key] = dictionary[key].replace('"', '\\"')
        elif isinstance(dictionary[key], list):
            for i in range(len(dictionary[key])):
                if isinstance(dictionary[key][i], dict):
                    # 如果当前值为字典类型，则进行递归调用
                    modify_dict(dictionary[key][i])
                elif isinstance(dictionary[key][i], str):
                    # 对于非字典类型的值，直接进行修改操作
                    dictionary[key][i] = dictionary[key][i].replace('"', '\\"')

    return dictionary


if __name__ == '__main__':

    pass
