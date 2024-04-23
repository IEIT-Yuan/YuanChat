import re, os
from rouge_score import rouge_scorer, tokenize
from transformers import BertTokenizer


class DataUtils:
    @staticmethod
    def split_segments(statement: str):
        all_statements = []
        statement = re.sub(' +', ' ', statement.replace('\n', ' '))
        split_pattern = r'(?<!\w\.\w.)(?<![A-Z]\.)(?<![A-Z][a-z]\.)(?<! [a-z]\.)(?<![A-Z][a-z][a-z]\.)(?<=\.|\?|\!)\"*\s*\s*(?:\W*)([A-Z])'
        tmp_statements = []
        
        for s in re.split(r"(\[\d+\])", statement):
        # for s in re.split(r"[。]", statement):
            if not s:
                continue
            cites = re.findall(r"\[(\d+)\]", s)
            if not cites: # Segment
                tmp_statements.append([s, []])
            elif not tmp_statements: # Citation Mark, but no Segments
                continue
            else: # Citation Mark
                for item in cites:
                    tmp_statements[-1][1].append(int(item) - 1)
        
        for s, cite in tmp_statements:
            prefix = ""
            for ix, seg in enumerate(re.split(split_pattern, s)):
                if len(prefix) > 20:
                    all_statements.append([prefix, []])
                    prefix = ""
                prefix += seg
                if prefix and prefix[-1] in ['.!?:']:
                    prefix += " "
            if prefix:
                if all_statements and len(prefix) < 20:
                    all_statements[-1][0] += prefix
                else:
                    all_statements.append([prefix, []])
            if all_statements:
                all_statements[-1][1] += cite
        
        return [seg[0] for seg in all_statements], [seg[1] for seg in all_statements]

    @staticmethod
    def split_segments_cn(statement: str):
        all_statements = []

        p_char = r'(！|。)'
        fields = re.split(p_char, statement)  # 多分隔符分割语句
        values_0 = fields[::2]  # 只包含诗句,list[start:end:step]
        if '' in values_0:
            values_0.remove('')
        delimiters_0 = fields[1::2]  # 只包含标点

        for va,de in zip(values_0,delimiters_0):
            all_statements.append(va+de)
        if all_statements == []:
            all_statements = [statement]

        return all_statements, [[] for seg in all_statements]

    @staticmethod
    def matching_score(all_statements, references, embeddings_model_path):
        def remove_stopwords(stmt: str):
            stmt = tokenize.tokenize(stmt, None)
            ret = []
            for item in stmt:
                if item in stopwords:
                    continue
                ret.append(item)
            return " ".join(ret)
            # return "".join(ret)  #中文
        
        # all_statements = [remove_stopwords(item) for item in all_statements]
        # references = [remove_stopwords(item) for item in references]
        
        # return None
        tokenizer = BertTokenizer.from_pretrained(embeddings_model_path)
        scorer = rouge_scorer.RougeScorer(['rouge1'], tokenizer=tokenizer)
        all_scores = []
        for statement in all_statements:
            # if len(tokenize.tokenize(statement, None)) < 5:
            #     all_scores.append([0] * len(references))
            #     continue
            ref_score = []
            for idx, ref in enumerate(references):
                rouge = scorer.score(ref, statement)['rouge1'].precision
                # print(rouge)
                ref_score.append(rouge)
            all_scores.append(ref_score)
        return all_scores
    
    @staticmethod
    def get_ideal_citations(all_scores, raw_citations, citation_threshold, extra_bonus=0.3):
        
        assert len(all_scores) == len(raw_citations)
        
        ideal_citations = []
        for seg_idx, scores in enumerate(all_scores):
            idc = []
            best_idx = 0
            best_scr = 0
            for idx, score in enumerate(scores):
                if idx in raw_citations[seg_idx]:
                    score += extra_bonus / len(raw_citations[seg_idx])
                if score >= citation_threshold:
                    idc.append(idx)
                if score > best_scr:
                    best_idx = idx
            if len(idc) == 0 and len(raw_citations[seg_idx]) > 0:
                idc.append(best_idx)
            ideal_citations.append(idc)
        return ideal_citations
    
    @staticmethod
    def recompose(all_statements, raw_citations, references, embeddings_model_path, sep=" ", citation_threshold=0.75) -> str:
        scores = DataUtils.matching_score(all_statements, references, embeddings_model_path)
        ret = ""
        ideal_citations = DataUtils.get_ideal_citations(scores, raw_citations, citation_threshold)

        # 若连续多句之间是同一个来源，则只保留最后一个即可
        if len(ideal_citations) > 1:
            ideal_citations_delrepeat = []
            for i in range(len(ideal_citations)-1):
                c_list = []
                for c in ideal_citations[i]:
                    if c not in ideal_citations[i+1]:
                        c_list.append(c)
                ideal_citations_delrepeat.append(c_list)
            ideal_citations_delrepeat.append(ideal_citations[-1])

        for seg, cit in zip(all_statements, ideal_citations):
            # judge if seg[0] is alphanumeric
            if ret and ret[-1] == "]" and seg and seg[0].isalnum():
                ret += sep
            ret += seg
            for c in cit:
                ret += "[%d]"%(c+1)
            if ret and ret[-1] in ".!?:":
                ret += sep
        return ret.strip()

class Stopwords:
    @staticmethod
    def load():
        #英文
        # src = [
        #     "./stopwords/english",
        #     "./stopwords/explaination",
        # ]
        #中文
        src = [
            os.path.join(os.path.dirname(__file__), "stopwords/chinese")
        ]
        ret = []
        for item in src:
            with open(item, "r", encoding='utf-8') as f:
                ret += [word.strip() for word in f.readlines()]
        return ret


stopwords = set(Stopwords.load())

def citation_correction(original_answer, references, embeddings_model_path):
    cites = re.findall(r"\[(\d+)\]", original_answer)
    if len(cites)>0:
        segments, raw_cite = DataUtils.split_segments(original_answer)
    else:
        segments, raw_cite = DataUtils.split_segments_cn(original_answer)
    
    return DataUtils.recompose(segments, raw_cite, references, embeddings_model_path)

if __name__ == "__main__":
    segments = [' 1加1等于2，在阿拉伯数字中只有1种答案。但是在不同的情境和语境下，1加1可以有多种不同的解读和答案。以下是一些有趣的例子：1. 在数学中，1加1等于2，这是一个基本的数学定理。[2]2. 在二进制计算中，1加1等于10。[2]\
3. 在时间单位不同的情况下，1加1可以有不同的答案。例如，1小时加1小时等于2小时，1分钟加1分钟等于2分钟，1秒加1秒等于2秒。[1] \
4. 在谜语和猜字游戏中，1加1可以有多种答案。例如，一加一等于十，表示数字10；一加一等于王、丰、卅等字形。[1]\
5. 在一些特殊情况下，1加1可以等于1。例如，当一堆沙倒入另一堆沙时，仍然是一堆沙。[1]\
6. 在单位不一致的情况下，1加1可以有多种答案。例如，1美元加1美元等于2美元，1千克加1千克等于2千克。[1]\
综上所述，1加1等于2是最常见的答案，但在不同的情境和语境下，它可以有多种不同的解读和答案。']


    references = ['1+1等于几?有多少种答案? 2023-01-05 16:07 2、单位不同时，如1小时加1分等于61分。 3、在急转弯时，如1加1,答案是11。 4、智力测验时，如一滴水加一滴水等于一滴水。 5、在猜字谜时，如一加1，答案是十。 6、一加一，答案是王、丰、卅等。 7、1+1=14（一周加一周是14天） 8、1+1=120（一分钟加一分钟是120秒） 9、1+1=7200（一个小时加上一个小时是7200秒） 10、1+1=60（一个30天的月加上另一个30天的月是60天） ；1+1=62（一个31天的月加上另一个31天的月是62天）。 11、1＋1＝10（计算机的二进制）。 12、1+1等于一， 因为一堆沙倒入一堆沙还是一堆。',
                  '1加1等于2，在阿拉伯数字中只有1种答案。因为在数学中1加1等于2是不变的定理，我们也没有必要再去深究，只要记着就行了。但是如果在计算机编程的情况下，如果用二进制表示 ...',
                  '一加一等于几有多少个答案？ 1+1等于几，有四种说法。第一种1+1等于2，第二种1+1等于11，第三种，1+1等于田。第四种，1+1，等于王。 妈妈问小明:1+1等于几，小明只顾吃饭,随口说:不知道。妈妈说:真是饭桶。妈妈又问:我跟你加起来是多少啊 ?小明答:两个饭桶 !']

    # DataUtils.recompose(segments, [[],[],[],[]], references)
    print('\n')
    print(citation_correction(segments[0], references, 'path'))
