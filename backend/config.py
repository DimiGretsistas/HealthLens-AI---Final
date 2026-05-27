import os
from dotenv import load_dotenv

from supadata import Supadata
from openai import OpenAI

from langchain_openai import ChatOpenAI
from langchain_openai import OpenAIEmbeddings


#Load environment variables
load_dotenv(".env", override=True)


#API clients
client = OpenAI()

supadata = Supadata(
    api_key=os.getenv("SUPADATA_API_KEY")
)


#LLM
llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0
)


#Embeddings
embeddings = OpenAIEmbeddings(
    model="text-embedding-3-small"
)


#Debug
print("OpenAI key loaded:", os.getenv("OPENAI_API_KEY") is not None)
print("Supadata key loaded:", os.getenv("SUPADATA_API_KEY") is not None)
