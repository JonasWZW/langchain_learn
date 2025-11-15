from dotenv import load_dotenv
import os

from langchain.chat_models import init_chat_model
from langchain_openai import ChatOpenAI

load_dotenv()
API_KEY = os.getenv("API_KEY")
BASE_URL = os.getenv("BASE_URL")
# print(f"{API_KEY} {BASE_URL}")

llm = init_chat_model(
    "deepseek-ai/DeepSeek-V3",
    model_provider="openai",
    base_url=BASE_URL,
    api_key=API_KEY,
    temperature=0
)