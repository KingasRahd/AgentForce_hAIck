from langchain_google_genai import ChatGoogleGenerativeAI
import os
from dotenv import load_dotenv
from test import p1

load_dotenv()
api_key=os.getenv('API_KEY')

model=ChatGoogleGenerativeAI(model='models/gemini-2.5-flash-lite-preview-06-17',google_api_key=api_key)

response=model.invoke(p1.format(country='China'))
print(response.content)
