from langchain_core.prompts import PromptTemplate
from langchain.output_parsers import StructuredOutputParser, ResponseSchema
from langchain_core.messages import AIMessage
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_together import ChatTogether
from langchain_community.document_loaders import TextLoader
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from dotenv import load_dotenv
from langchain_experimental.text_splitter import SemanticChunker
from langchain.retrievers.document_compressors import LLMChainExtractor
from langchain.retrievers.contextual_compression import ContextualCompressionRetriever
import os
import shutil

load_dotenv()

huggingface_api = os.getenv("LANCHAIN_HUGGINGFACE_API_KEY")

together_api = os.getenv("TOGETHER_AI_API_KEY")

class QuestionAnswer:
    def __init__(self):
        self.model_H = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
        self.model_T = ChatTogether(
            model="deepseek-ai/DeepSeek-R1-Distill-Llama-70B-free",
            api_key=together_api,
            timeout=600,
            temperature=0.7
        )
        self.compressor = LLMChainExtractor.from_llm(self.model_T)
        self.file_path = "ai_backend/scraped_output.txt"
        self.schema = [
            ResponseSchema(name="Answer", description="Tell me the answer about my query from the given data and try to understand the query meaning and give the accurate answer of the query instead of long answer")
        ]
        self.parser = StructuredOutputParser.from_response_schemas(self.schema)

        self.data = self.get_data()
        self.split = self.text_splitter()
        self.store = self.vector_store() 

    def get_data(self):
        loader = TextLoader(self.file_path, encoding="utf-8")
        docs = loader.load()
        return "\n".join([doc.page_content for doc in docs])

    def text_splitter(self):
        splitter = SemanticChunker(self.model_H)
        chunks = splitter.split_text(self.data)
        return chunks

    def vector_store(self):
        persist_dir = "faiss_db"
        if os.path.exists(persist_dir):
            print("Loading existing FAISS db")
            return FAISS.load_local(
                persist_dir, 
                self.model_H, 
                allow_dangerous_deserialization=True  # 👈 Add this line
            )
        else:
            print("Creating new FAISS db")
            store = FAISS.from_texts(self.split, self.model_H)
            store.save_local(persist_dir)
            return store


    def get_similars(self, question, k):
        base_retriever = self.store.as_retriever(
            search_typer = "similar",
            search_kwargs = {"k":10 , "lambda_mult" : 0.9}
        )
        compressor_retriever = ContextualCompressionRetriever(
            base_retriever= base_retriever,
            base_compressor= self.compressor
        )
        return compressor_retriever.invoke(question)

    def template(self, db_docs, question):
        prompt = (
            f"You are a helpful assistant. Answer the given question strictly based **only** on the following Available Web Content Data text:\n\n"
            f"{[doc.page_content for doc in db_docs]}\n\n"
            "Respond with a markdown code snippet formatted in **strict JSON**, following this exact schema.\n"
            "Make sure your answer is derived from the given data and state that explicitly.\n\n"
            "```json\n"
            "{\n"
            '  "Answer": "string (Tell me the answer about my query from the given data and try to understand the query meaning and give the accurate answer of the query instead of long answer , Do NOT use outside knowledge. Mention that this is based on the provided Web Content data in Answer in Last line.)"\n'
            "}\n"
            "```"
        )
        return prompt

    def run_qa(self, question, k=20):
        db = self.get_similars(question, k)
        prompt = self.template(db, question)
        result = self.model_T.invoke(prompt)

        if isinstance(result, AIMessage):
           result = result.content

        return self.parser.parse(result).get("Answer")
        
            