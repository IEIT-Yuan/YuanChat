import time
import os
import yaml
import re
from web_argumnet.fetch_web_content import WebContentFetcher
from web_argumnet.retrieval import EmbeddingRetriever
from web_argumnet.langchain_yuan import Yuan2
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.schema import HumanMessage
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler

class LLMAnswer:
    # TOP_K = 3  # Top K documents to retrieve

    def __init__(self, paras_dict):
        # # old: Load configuration from a YAML file
        # config_path = os.path.join(os.path.dirname(__file__), 'config', 'config.yaml')
        # with open(config_path, 'r') as file:
        #     self.config = yaml.safe_load(file)
        # self.model_name = self.config["model_name"]
        # self.api_key = self.config["openai_api_key"]

        #从网页加载参数
        self.TOP_K = paras_dict["retrieve_topk"]    # Top K documents to retrieve
        self.model_name = "yuan2"
        self.template = paras_dict["template"]

    def _format_reference(self, relevant_docs_list, link_list):
        # Format the references from the retrieved documents for use in the prompt
        self.TOP_K = min(self.TOP_K, len(relevant_docs_list))
        reference_url_list = [(relevant_docs_list[i].metadata)['url'] for i in range(self.TOP_K)]
        reference_content_list = [relevant_docs_list[i].page_content for i in range(self.TOP_K)]

        # # 去除重复内容
        # reference_content_list_new = []
        # reference_url_list_new = []
        # for i in range(self.TOP_K):
        #     if reference_content_list[i] not in reference_content_list_new:
        #         reference_content_list_new.append(reference_content_list[i])
        #         reference_url_list_new.append(reference_url_list[i])
        # reference_url_list = reference_url_list_new
        # reference_content_list = reference_content_list_new

        try:
            reference_index_list = [link_list.index(link)+1 for link in reference_url_list]
            rearranged_index_list = self._rearrange_index(reference_index_list)
        except:
            rearranged_index_list = [i+1 for i in range(len(reference_url_list))]

        # Create a formatted string of references
        formatted_reference = "\n"
        for i in range(len(reference_url_list)):
            formatted_reference += ('Webpage[' + str(rearranged_index_list[i]) + '], url: ' + reference_url_list[i] + ':\n' + reference_content_list[i][:300] + '\n\n\n')
            # formatted_reference += ('Webpage[' + str(rearranged_index_list[i]) + '], url: ' + reference_url_list[i] + ':\n' + reference_content_list[i] + '\n\n\n')
        return formatted_reference

    def _rearrange_index(self, original_index_list):
        # Rearrange indices to ensure they are unique and sequential
        index_dict = {}
        rearranged_index_list = []
        for index in original_index_list:
            if index not in index_dict:
                index_dict.update({index: len(index_dict)+1})
                rearranged_index_list.append(len(index_dict))
            else:
                rearranged_index_list.append(index_dict[index])
        return rearranged_index_list


    def get_answer_yuan(self, query, relevant_docs, language, paras_dict):
        # Create an instance of Yuan and generate an answer
        output_format =  ""
        profile = ""

        # llm = Yuan2(infer_api="http://172.31.4.32:8900/yuan", max_tokens=2048, temp=1.0, top_p=0.8, top_k=0, use_history=False)
        llm = Yuan2(infer_api=paras_dict["url"][0][0], max_tokens=paras_dict["response_length"],
                    temp=paras_dict["temperature"], top_p=paras_dict["top_p"], top_k=paras_dict["top_k"], use_history=False)

        profile = "认真的研究者" if not profile else profile

        # 如果是中文问题，使用中文模板
        pattern = re.compile(r'[\u4e00-\u9fff]+')
        if bool(pattern.search(query+self.template)):
            template = "Web搜索结果：\n{context_str}\n\n" + self.template + "{query}\n答案："
        else:
            template = "Web search result:\n{context_str}\n\n" + self.template + "{query}\nAnswer:"

        prompt_template = PromptTemplate(
            input_variables=["profile", "context_str", "language", "query", "format"],
            template=template
        )
        summary_prompt = prompt_template.format(context_str=relevant_docs, query=query, format=output_format, profile=profile)
        print("\n\n输入LLM文本：\n", summary_prompt)
        print("\n\n", "="*30, "YUAN答案：", "="*30, "\n")

        yuan_answer = llm(summary_prompt)
        print(yuan_answer)

        return yuan_answer, summary_prompt


# Example usage
if __name__ == "__main__":
    paras_dict = {}
    content_processor = LLMAnswer(paras_dict)
    query = "What happened to Silicon Valley Bank"
    output_format = "" # User can specify output format
    profile = "" # User can define the role for LLM

    # Fetch web content based on the query
    web_contents_fetcher = WebContentFetcher(query)
    web_contents, serper_response = web_contents_fetcher.fetch()

    # Retrieve relevant documents using embeddings
    retriever = EmbeddingRetriever()
    relevant_docs_list = retriever.retrieve_embeddings(web_contents, serper_response['links'], query)
    formatted_relevant_docs = content_processor._format_reference(relevant_docs_list, serper_response['links'])
    print(formatted_relevant_docs)

    # Measure the time taken to get an answer from the LLM model
    start = time.time()

    # Generate answer from ChatOpenAI
    ai_message_obj = content_processor.get_answer_yuan(query, formatted_relevant_docs, serper_response['language'], paras_dict)
    answer = ai_message_obj.content + '\n'
    end = time.time()
    print("\n\nLLM Answer time:", end - start, "s")