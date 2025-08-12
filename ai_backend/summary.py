from langchain_core.prompts import PromptTemplate
from langchain.output_parsers import StructuredOutputParser , ResponseSchema
from langchain_core.messages import SystemMessage , HumanMessage , AIMessage
from langchain_together import ChatTogether
from langchain_community.document_loaders import TextLoader
from langchain.schema.runnable import RunnableParallel , RunnableSequence
from dotenv import load_dotenv
import os
import re

load_dotenv()

together_api = os.getenv("TOGETHER_AI_API_KEY")


class TextSummarizer:
    def __init__(self):
        self.model = ChatTogether(
            model = "deepseek-ai/DeepSeek-R1-Distill-Llama-70B-free",
            api_key=together_api,
            timeout= 300,
            temperature=0.7
        )
        schema = [ResponseSchema(name="summary" , description= "A List of short summary for each phases of the text provided to you ")]
        
        self.parser = StructuredOutputParser.from_response_schemas(schema)

        self.prompt = PromptTemplate(
            template="""You are an AI Text Summarizer. Read the input text and provide a clear, concise summary that captures the key points, making it quick and easy for a human to understand in less time. Keep the summary short, informative, and easy to read. \n from the following the \n {text} , \n {formatted_output}
            """,
            input_variables=["text"],
            partial_variables={"formatted_output" : self.parser.get_format_instructions()}
        )

    def word_limit_set(self, text, limit):
        words = text.split()
        limited_text = " ".join(words[:limit])
        
        # Ensure it's under a certain number of characters
        if len(limited_text) > limit:
            limited_text = limited_text[:limit]  # Cutting by character length
        
        return limited_text

    
    def summarize_file(self , path):
        loader = TextLoader(path , encoding= "utf-8")
        docs = loader.load()

        # Convert list of Document objects into plain text
        text = "\n".join([doc.page_content for doc in docs])
        text = re.sub(r'\s+', ' ', text).strip()
        limlited_text = self.word_limit_set(text , 15000)
        print(limlited_text)
        print(type(limlited_text))
        print(len(limlited_text))
        
        chain = self.prompt | self.model | self.parser
        output = chain.invoke({"text": limlited_text})


        if isinstance(output, dict) and "summary" in output:
            return output["summary"]
        else:
            # Fallback behavior: return the raw output or raise a descriptive error
            print("Warning: Output is not structured as expected.")
            print("Raw output:", output)
            return output  # or raise Exception("Unexpected model output format")



