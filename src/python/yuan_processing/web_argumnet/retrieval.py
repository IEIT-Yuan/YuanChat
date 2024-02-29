import yaml
import os
from web_argumnet.fetch_web_content import WebContentFetcher
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings
from langchain.embeddings.sentence_transformer import SentenceTransformerEmbeddings

class EmbeddingRetriever:
    # TOP_K = 3  # Number of top K documents to retrieve

    def __init__(self, paras_dict):
        # # Load configuration from config.yaml file
        # config_path = os.path.join(os.path.dirname(__file__), 'config', 'config.yaml')
        # with open(config_path, 'r') as file:
        #     self.config = yaml.safe_load(file)

        self.retrieve_topk = paras_dict["retrieve_topk"]
        self.embeddings_model_path = paras_dict["embeddings_model_path"]
        self.TOP_K = 3
        # Initialize the text splitter
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=0
        )

    def retrieve_embeddings(self, contents_list: list, link_list: list, query: str):
        # Retrieve embeddings for a given list of contents and a query
        metadatas = [{'url': link} for link in link_list]
        texts = self.text_splitter.create_documents(contents_list, metadatas=metadatas)

        # Create a Chroma database from the documents using specific embeddings
        db = Chroma.from_documents(
            texts,

            # Select one of the models from OpenAIEmbeddings and text2vec-base-chinese to suit your needs:
            
            # OpenAIEmbeddings(model='text-embedding-ada-002', openai_api_key=self.config["openai_api_key"])
            SentenceTransformerEmbeddings(model_name=self.embeddings_model_path)
        )

        # Create a retriever from the database to find relevant documents
        # retriever = db.as_retriever(search_kwargs={"k": self.TOP_K})
        retriever = db.as_retriever()
        return retriever.get_relevant_documents(query) # Retrieve and return the relevant documents


    def retrieve_embeddings_noreapt(self, contents_list: list, link_list: list, query: str):
        # Retrieve embeddings for a given list of contents and a query
        metadatas = [{'url': link} for link in link_list]
        texts = self.text_splitter.create_documents(contents_list, metadatas=metadatas)

        # Create a Chroma database from the documents using specific embeddings
        db = Chroma.from_documents(
            texts,

            # Select one of the models from OpenAIEmbeddings and text2vec-base-chinese to suit your needs:

            # OpenAIEmbeddings(model='text-embedding-ada-002', openai_api_key=self.config["openai_api_key"])
            SentenceTransformerEmbeddings(model_name=self.embeddings_model_path)
        )

        # Create a retriever from the database to find relevant documents
        retriever = db.as_retriever(search_kwargs={"k": len(contents_list)})
        all_docs = retriever.get_relevant_documents(query)

        # 去重
        relevant_docs_list = []
        for doc in all_docs:
            if doc not in relevant_docs_list:
                relevant_docs_list.append(doc)

        self.TOP_K = min(self.retrieve_topk, len(relevant_docs_list))

        return relevant_docs_list[:self.TOP_K]


    # Example usage
if __name__ == "__main__":
    query = "What happened to Silicon Valley Bank"

    # Create a WebContentFetcher instance and fetch web contents
    web_contents_fetcher = WebContentFetcher(query)
    web_contents, serper_response = web_contents_fetcher.fetch()

    # Create an EmbeddingRetriever instance and retrieve relevant documents
    paras_dict = {}
    retriever = EmbeddingRetriever(paras_dict)
    relevant_docs_list = retriever.retrieve_embeddings(web_contents, serper_response['links'], query)

    print("\n\nRelevant Documents from VectorDB:\n", relevant_docs_list)
    