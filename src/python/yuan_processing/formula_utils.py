# coding:utf-8
import re
formula_pattern = r'([a-zA-Z0-9α ∃∀∋∈∩∪ξπωφ×∧′⋅•^%.&!,=═_+÷:;㎡²³☆★▲△□℃*…（ ）/<>\'\-\(\)\[\]\{\}\|\\]{1,})'
#\w:匹配字母或数字或下划线或汉字
# ret_compile = re.compile("(?P<s>[\\\\]*)(?P<start>[a-zA-Z0-9<>()\[\]\-⟨∣∥{}⌊⌈∑∏′∫∬∭∮∇∵∴∀∃∨∧⋁⋀αβΓγΔδϵεζηΘθικΛλμνΞξΠπρΣστΦϕφχΨψΩω|=-])"
#                          "(?P<content>[^\u4E00-\u9FA5\r\n\f\v、：；《》。，！？“”‘’【】（）]{1,})")
ret_compile = re.compile("(?P<content>[^\u4E00-\u9FA5\r\n\f\v、：；《》。，！？“”‘’【】（）]{2,})")

# 上下标符号 a_0,a^0
symbols00 = list('_^')
# 括号/取整符号
parenthesis_rounding_markdown = ['(, )', '[, ]', '\lang', '\rang', '\langle', '\rangle']
symbols0 = list('()[]⟨⟩∣∥{}⌊⌋⌈⌉')
# 累加、累乘
symbols1 = list('∑∏')
# 二元运算符
symbols2 = list('±∓×÷∗⋆∣∤∘∙⋅≀⋄◊△△▽◃▹⊲⊳⊴⊵∘◯⊙⨀⊘⊖⊗⨂⊕⨁†‡⨿')
# 关系符号
symbols3 = list('≤≥≡⊨≺≻∼⊥⪯⪰≃∣≪≫≍∥≈≅≠≐∝⋈⊢⊣')
# 极限
symbols4 = list('→∞')
# 微积分
symbols5 = list('′∫∬∭∮∇')
# 箭头
symbols6 = list('↑↓↕⇑⇓⇕→←↔⇒⇐⇔⟶⟵⟷⟹⟸⟺↦⟼↩↪⇀↽⇌↼⇁⇝↗↘↙↖')
# 集合
symbols7 = list('∅∈∋∉⊂⊃⊄⊆⊇∪⋃∩⋂⊎⨄⊏⊐⊓⊑⊒∨∧∖')
# 逻辑运算
symbols8 = list('∵∴∀∃∨∧⋁⋀')
# 希腊字母
symbols9 = list('αβΓγΔδϵεζηΘθικΛλμνΞξΠπρΣστΦϕφχΨψΩω')
# 省略号
symbols10 = list('…⋯⋮⋱')
# 其他符号
symbols11 = list('ℵℏıȷℓ℘ℜℑ℧∇√⊤⊥¬♭♮♯\∂□♣♢♡♠')
# else号
symbols12 = list('•.&!@#%?,=═+*:;㎡²³☆★▲℃（ ）<>-\|～')
# Markdown 支持以下这些符号前面加上反斜杠来帮助插入普通的符号 [* . ? + $ ^ [ ] ( ) { } | \ /-]
# \   反斜线；`   反引号*   星号；_   底线；{}  花括号；[]  方括号；()  括弧；#   井字号；+   加号；-   减号；.   英文句点；!   惊叹号；


#检查大括号是否成对
def check_bracket_couple(str_in):
    ret = 0
    ret += str_in.count("{")
    ret -= str_in.count("}")
    return ret


#检查是否为纯英文单词
def is_pure_word(str_in):
    pattern = r"[a-zA-Z ]{1,}"
    match_ret = re.fullmatch(pattern, str_in)
    if match_ret is None:
        return False
    else:
        return True

#检查是否存在单词字符和希腊字母
def is_pure_symbols(str_in):
    pattern = r"[a-zA-Z0-9αβΓγΔδϵεζηΘθικΛλμνΞξΠπρΣστΦϕφχΨψΩω]{1,}"
    match_ret = re.search(pattern, str_in)
    if match_ret is None:
        return False
    else:
        return True


#检查是否存在运算符号
def is_symbols_exist(str_in):
    # pattern = r"[^A-Za-z0-9\u4E00-\u9FA5\r\n\f\v、：；《》。，！？“”‘’【】（）]{1,}"
    # pattern = r"[∃∀∋∈∩∪ξπωφ×∧′⋅•\^%&!,=═_+;*/<>\']{1,}"
    pattern = r"[\^_∣∥⌊⌋⌈⌉∑∏±∓×÷∗⋆∤∘∙⋅≀⋄◊△▽◃▹⊲⊳⊴⊵∘◯⊙⨀⊘⊖⊗⨂⊕⨁†‡⨿≤≥≡⊨≺≻∼⊥⪯⪰≃≪≫≍∥≈≅≠≐∝⋈⊢⊣→∞′∫∬∭∮∇∅∈∋∉⊂⊃⊄⊆⊇∪⋃∩⋂⊎⨄⊏⊐⊓⊑⊒∨∧∖∀∃∨∧⋁⋀…⋯⋮⋱&!=═+*<>㎡²³℃\-—|/～\[\\]{1,}"

    match_ret = re.search(pattern, str_in)
    if match_ret is None:
        return False
    else:
        return True


#检查是否为纯数字，包括整数、小数、百分数
def is_pure_number(str_in):
    pattern = r"^(\-|\+)?\d+(\.\d+)?%?$"
    match_ret = re.fullmatch(pattern, str_in)
    if match_ret is None:
        return False
    else:
        return True


#删除字符中前后包含的英文单词
def remove_words(str_in):
    str_out = str_in.strip()
    str_out = re.sub(r'^[A-Za-z]+ ([A-Za-z]+ )*([A-Za-z]+)', r'\2', str_out)  # ^ :匹配字符串开头
    str_out = re.sub(r'( [A-Za-z]+ )([A-Za-z]+ )*([A-Za-z]+)$', r'\1', str_out)  # ^ :匹配字符串结尾
    str_out = str_out.strip()
    return str_out


# 删除误识别情况
def remove_speclai_formula(str_in):
    str_out = str_in.strip()
    if str_out is None:
        return None

    # (1) 公式中全是英文单词（误识别英文语句）
    pattern1 = r'[a-zA-Z.,;:?\'" ]+'  #英文表达中常见标点
    match_ret = re.fullmatch(pattern1, str_out)
    if match_ret is not None:
        return None

    # （2）去除前后误加入的英文单词
    str_out = remove_words(str_out)

    # # (3)公式中全是非单词字符或空白字符
    # match_ret = re.fullmatch(r'[\W\s]{1,}', str_out)
    # if match_ret is not None:
    #     return None

    # (4) 检查纯数字
    if is_pure_number(str_out):
        return None

    # 检查是否存在单词字符和希腊字母，若是TRUE，表示含有
    if is_pure_symbols(str_out) == False:
        return None

    # 检查是否存在运算符号
    if is_symbols_exist(str_out) == False:
        return None

    # 检查序号类，如(3) 3) (3 B. [2] 2]
    str_out = re.sub(r'^\(?[A-Za-z0-9. ]+\)?$', r'', str_out)  # ^ :匹配字符串开头 $：匹配字符串结尾 (3 )  (3.1 ) (3a
    str_out = re.sub(r'^\[?[A-Za-z0-9. ]+]?$', r'', str_out)  # 去除 [2] 2]  [2

    # 去掉<n> 前后的序号 如 1.<n>xxxxxx <n>2. xxxxxxx
    str_out = re.sub(r'[0-9]+\.<n>', r'', str_out)
    str_out = re.sub(r'<n>[0-9]+\.', r'', str_out)

    # # 删除GPT-4情况
    # pattern1 = r"[a-zA-Z]+-[0-9]+"
    # match_ret = re.fullmatch(pattern1, str_out)
    # if match_ret is not None:
    #     return None

    # 误识别英文语句 / would/could/should/might have
    pattern1 = r"[a-zA-Z /]{1,}"
    match_ret = re.fullmatch(pattern1, str_out)
    if match_ret is not None:
        return None

    # 若公式中存在的单词长度大于总长度的一半，认为是英文语句，删除
    str_out_bak = ' ' + str_out.replace(' ', '  ')
    pattern1 = r' [a-zA-Z]+[, .]'  # 英文表达中常见标点
    match_ret = re.findall(pattern1, str_out_bak)
    sum = 0
    for ret in match_ret:
        sum += len(ret.strip())
    if sum > len(str_out) / 2:
        return None

    # 误识别英文语句+ $C++ IDE$
    pattern1 = r"C\+\+[A-Za-z ]*"
    match_ret = re.fullmatch(pattern1, str_out)
    if match_ret is not None:
        return None

    # 误识别英文最后是标点符号 “ $since+$ 一段时间+ago”   录出了 $mRNA--$ 分子杂交技术  使用倍数；twice  $as…$ 意为“是…的两倍”；
    pattern1 = r"[A-Za-z ]+[ \+\-…]+"
    match_ret = re.fullmatch(pattern1, str_out)
    if match_ret is not None:
        return None

    # 爱立信的 $LTE/4G$ 基站将开始在英国投入使用
    pattern1 = r"[A-Za-z ]{1,}/[A-Za-z0-9]{1,}"
    match_ret = re.fullmatch(pattern1, str_out)
    if match_ret is not None:
        return None

    if len(str_out) <= 2:  #长度至少3，否则如T5会被误识别
        return None

    return str_out


#查找文本中的数学公式
def find_math_formula(text):

    tail_text = text
    formula_arry = []

    while True:
        match_object = ret_compile.search(tail_text)
        # match_object = re.search(formula_pattern, tail_text)

        if match_object is not None:
            formula = tail_text[match_object.start():match_object.end()]
            tail_text = tail_text[match_object.end():]

            kuohao_index = -1
            if formula.count('{') > formula.count('}') and '}' in tail_text:  #{}凑成一对
                kuohao_index = tail_text.index('}')
            elif formula.count('(') > formula.count(')') and ')' in tail_text:  #()凑成一对
                kuohao_index = tail_text.index(')')
            if kuohao_index > 0 and kuohao_index < 20:    #小于10个字符，归于一个公式。太长的话分属两个
                formula = formula + tail_text[0:kuohao_index+1]
                tail_text = tail_text[kuohao_index+1:]

                # ret_compile1 = re.compile("[^\u4E00-\u9FA5\r\n\f\v、：；《》。，！？“”‘’【】（）]{1,}")
                # match_object1 = ret_compile1.search(tail_text)
                # if match_object1 is not None and match_object1.start() == 0:
                #     formula = formula + tail_text[match_object1.start():match_object1.end()]
                #     tail_text = tail_text[match_object1.end():]

            formula_arry.append(formula)
        else:
            break

    # 去除异常情况
    formula_arry_final = []
    for str_formula in formula_arry:
        tmp = str_formula
        tmp = remove_speclai_formula(tmp)

        if tmp is not None :
            match_object = ret_compile.search(tmp)
            if match_object is not None:
                formula_arry_final.append(tmp)
    return formula_arry_final


# 如果输出本身带有$，用自身的$，但是需在$后面加空格
def add_blank_to_formula(in_text):
    in_text = in_text.replace('\\n', '\n')
    in_text = re.sub(r'(\n{2,})', r'\n', in_text)  # 两个以上的连续换行符只保留一个

    # 前后都加空格，公式内部添加空格无影响
    in_text = in_text.replace('$$', '￥￥')
    text_with_blank = in_text.replace('$', ' $ ')
    text_with_blank = re.sub('[ \n]*￥￥[ \n]*', ' $$ ', text_with_blank)  #?表示匹配0次或1次
    text_with_blank = re.sub(r' {2,}', r' ', text_with_blank) #删除多余空格

    return text_with_blank


# 公式检索及后处理主函数
def add_dollor_to_formula(text):
    text = text.strip().replace('<eod>', '').replace('<n>', '\n')

    # 检索公式位置，并添加$
    text_pro = text.replace('$', '').replace('\\n', '\n')  # 去除$符号的干扰
    text_pro = re.sub(r'(\n{2,})', r'\n', text_pro)  # 两个以上的连续换行符只保留一个
    text_pro = re.sub(r'( {2,})', r' ', text_pro)  # 两个以上的连续空格符只保留一个

    # python 转义字符替换，正则匹配时转义字符会被跳过
    # \n：换行  \a：响铃  \b：退格(Backspace)  \e：转义 \000：空 \v：纵向制表符 \t：横向制表符 \r：回车 \f：换页 \oyy：八进制数，yy代表的字符，例如：\o12代表换行 \xyy：十六进制数，yy代表的字符，例如：\x0a代表换行
    # text_with_dollor = text_with_dollor.replace('\a', '\\a').replace('\b', '\\b').replace('\e', '\\e').replace('\v', '\\v').replace('\t', '\\t').replace('\r', '\\r').replace('\f', '\\f')
    text_pro = re.sub(r'\a([a-z])', r'\\a\1', text_pro)  #只匹配替换markdown表示的转义字符
    # text_with_dollor = re.sub(r'\b([a-z])', r'\\b\1', text_with_dollor)  # 只匹配替换markdown表示的转义字符
    # text_with_dollor = re.sub(r'\e([a-z])', r'\\e\1', text_with_dollor)
    text_pro = re.sub(r'\v([a-z])', r'\\v\1', text_pro)
    text_pro = re.sub(r'\t([a-z])', r'\\t\1', text_pro)
    text_pro = re.sub(r'\r([a-zV])', r'\\r\1', text_pro)
    text_pro = re.sub(r'\f([a-z])', r'\\f\1', text_pro)
    text_pro = re.sub(r'\n(mid|eq|earrow|warrow|i|ot|abla|u|eg|atural)', r'\\n\1', text_pro)
    text_pro = text_pro.replace('\b', '\\b').replace('\e', '\\e')  #\b无法用匹配方式，会多出很多匹配；\e无法用匹配方式，报错

    formula_arry = find_math_formula(text_pro)
    # formula_arry.sort(key=(lambda str: len(str)), reverse=True)

    tail_text = text_pro
    head_text = ''
    for i in range(0, len(formula_arry)):
        formula = formula_arry[i]

        pos = tail_text.find(formula)
        if pos < 0 or pos > len(tail_text):
            continue

        head_text += tail_text[:pos] + ' $' + formula.strip('$')  + '$ '
        tail_text = tail_text[pos+len(formula):]

    text_with_dollor = head_text + tail_text
    text_with_dollor = re.sub(r'\$([ ,]+)\$', r'\1', text_with_dollor)   #两个相连合并为一个公式
    print(text_with_dollor)
    return text_with_dollor



if __name__ == '__main__':

    # 直接输入list测试
    input_list = ['本题考查的知∃ ∃∃识点是∃ a∃∃归纳推理this is \nmid800{米}\nabla(x)-y\neg\natural',
                  '改进技术后的零件现在的成本是280 元减去改进后零件的成本25%，即：\n280 元－25%=230 元\n因此，现在这种零件的成本是230 元。',
                  '长方形的面积为：\n220 × 60 = 1200\n因此，原绳子的长度是 50 厘米。']
    for in_text in input_list:
        out_text = add_dollor_to_formula(in_text)
        print(out_text)

    pass

    # #读取文档测试
    # with open(r'D:\E\Code\NLP\yuan-zhanting-update\yuan-algorithm\test_files\chi_all_true_res_new.txt', 'r', encoding='UTF-8') as fr:
    #     lines = fr.readlines()
    #
    # for line in lines[0:100]:
    #     in_text = line.strip()
    #     out_text = add_dollor_to_formula(in_text)
    #
    #     # print(out_text)
    #     print('-------------------')

