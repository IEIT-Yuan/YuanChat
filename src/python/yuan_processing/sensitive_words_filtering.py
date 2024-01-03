# -*- coding:utf-8 -*-
import os
import time
AS_HOME_DIR = os.path.dirname(__file__)


# DFA算法
class DFAFilter(object):
    def __init__(self):
        self.keyword_chains = {}  # 关键词链表
        self.delimit = '\x00'  # 限定

    def add(self, keyword):
        keyword = keyword.lower()  # 关键词英文变为小写
        chars = keyword.strip()  # 关键字去除首尾空格和换行
        if not chars:  # 如果关键词为空直接返回
            return
        level = self.keyword_chains
        # 遍历关键字的每个字
        for i in range(len(chars)):
            # 如果这个字已经存在字符链的key中就进入其子字典
            if chars[i] in level:
                level = level[chars[i]]
            else:
                if not isinstance(level, dict):
                    break
                for j in range(i, len(chars)):
                    level[chars[j]] = {}
                    last_level, last_char = level, chars[j]
                    level = level[chars[j]]
                last_level[last_char] = {self.delimit: 0}
                break
        if i == len(chars) - 1:
            level[self.delimit] = 0

    def parse(self, path_list):
        for path in path_list:
            with open(os.path.join(AS_HOME_DIR, "data", path), encoding='utf-8') as f:
                for keyword in f:
                    self.add(str(keyword).strip())
            # print(self.keyword_chains)

    def filter(self, message, repl="*", out_sens=False):
        message = message.lower()
        ret = []
        ret_sens = []
        start = 0
        flag = False
        while start < len(message):
            level = self.keyword_chains
            step_ins = 0
            for char in message[start:]:
                if char in level:
                    step_ins += 1
                    if self.delimit not in level[char]:
                        level = level[char]
                    else:
                        ret_sens.append(message[start:start + step_ins])
                        ret.append(repl * step_ins)
                        start += step_ins - 1
                        flag = True
                        break
                else:
                    ret.append(message[start])
                    break
            else:
                ret.append(message[start])
            start += 1

        if out_sens:
            return ''.join(ret), flag, ret_sens
        return ''.join(ret), flag


# AC自动机过滤敏感词算法
class node(object):
    def __init__(self):
        self.next = {}
        self.fail = None
        self.isWord = False
        self.word = ""

class ac_automation(object):

    def __init__(self):
        self.root = node()

    # 添加敏感词函数
    def addword(self, word):
        temp_root = self.root
        for char in word:
            if char not in temp_root.next:
                temp_root.next[char] = node()
            temp_root = temp_root.next[char]
        temp_root.isWord = True
        temp_root.word = word

    # 失败指针函数
    def make_fail(self):
        temp_que = []
        temp_que.append(self.root)
        while len(temp_que) != 0:
            temp = temp_que.pop(0)
            p = None
            for key,value in temp.next.item():
                if temp == self.root:
                    temp.next[key].fail = self.root
                else:
                    p = temp.fail
                    while p is not None:
                        if key in p.next:
                            temp.next[key].fail = p.fail
                            break
                        p = p.fail
                    if p is None:
                        temp.next[key].fail = self.root
                temp_que.append(temp.next[key])

    # 查找敏感词函数
    def search(self, content):
        p = self.root
        result = []
        currentposition = 0

        while currentposition < len(content):
            word = content[currentposition]
            while word in p.next == False and p != self.root:
                p = p.fail

            if word in p.next:
                p = p.next[word]
            else:
                p = self.root

            if p.isWord:
                result.append(p.word)
                p = self.root
            currentposition += 1
        return result

    # 加载敏感词库函数
    def parse(self, path_list):
        for path in path_list:
            with open(path,encoding='utf-8') as f:
                for keyword in f:
                    self.addword(str(keyword).strip())

    # 敏感词替换函数
    def words_replace(self, text):
        """
        :param ah: AC自动机
        :param text: 文本
        :return: 过滤敏感词之后的文本
        """
        result = list(set(self.search(text)))
        result = [i for i in result if i != '']
        for x in result:
            m = text.replace(x, '*' * len(x))
            text = m
        return text


if __name__ == "__main__":
    gfw = DFAFilter()
    path_list = ['bad-words-adver.txt', 'bad-words-politic.txt', 'bad-words-violence.txt', 'bad-words-porn.txt']
    gfw.parse(path_list)
    text="梦里田园历乱春，醒来几度认荒坟。他乡作客曾无数，此日依乡独未归。添白发，叹青山。怜他老大尚多情。窗前浊酒浇斜日，山色欲明雾露深。"
    result, flag = gfw.filter(text)  #flag为true表示包含敏感信息，否则无
    print(result)

