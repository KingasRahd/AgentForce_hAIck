
from langchain_google_genai import ChatGoogleGenerativeAI
import os
from dotenv import load_dotenv
import prompts
from langchain_core.output_parsers import StrOutputParser
from langchain.schema.runnable import RunnableParallel,RunnablePassthrough
from operator import itemgetter
import json

load_dotenv()
api_key=os.getenv('API_KEY')

model=ChatGoogleGenerativeAI(model='models/gemini-2.5-flash-lite-preview-06-17',google_api_key=api_key)
parser=StrOutputParser()


def llm(query):
    parallel_chain=RunnableParallel(
        {
            'courses':prompts.course_suggestion|model|parser,
            'online_certifications':prompts.online_certification|model|parser,
            'projects':prompts.projects|model|parser,
            'roadmap':RunnablePassthrough()
        }
    )

    chain=prompts.start|model|parser|parallel_chain|{
        'courses':itemgetter('courses'),
        'online_certifications':itemgetter('online_certifications'),
        'projects':itemgetter('projects'),
        'roadmap':itemgetter('roadmap')
    }|prompts.final|model|parser

    response=chain.invoke({'query':query})
    return response



response=llm("i want to learn Wev Dev")
print(response)

