import os
from dotenv import load_dotenv
from langchain.chat_models import ChatOpenAI

load_dotenv()

llm = ChatOpenAI(
    model="gpt-4",
    temperature=0.2,
    openai_api_key=os.getenv("OPENAI_API_KEY")
)
