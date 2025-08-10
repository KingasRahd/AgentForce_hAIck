from flask import Flask,render_template,request,jsonify
from langchain_google_genai import ChatGoogleGenerativeAI
import os
from dotenv import load_dotenv
import prompts
from langchain_core.output_parsers import StrOutputParser
from langchain.schema.runnable import RunnableParallel,RunnablePassthrough
from operator import itemgetter
import json
import sys
import sqlite3

response=''
load_dotenv()
api_key=os.getenv('API_KEY')

model=ChatGoogleGenerativeAI(model='models/gemini-2.5-flash-lite-preview-06-17',google_api_key=api_key)
parser=StrOutputParser()

conn=sqlite3.connect("hAIck.db")
cursor=conn.cursor()


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


def db_store(response):

    cursor.execute("""
CREATE TABLE IF NOT EXISTS tasks(
                  id INTEGER PRIMARY KEY AUTOINCREMENT,
                   step INTEGER,
                   type TEXT,
                   task TEXT,
                   status TEXT
                   )
""")
    
    jsoned=json.loads(response)

    for i in jsoned:
        step_no=i['step_number']

        for course in i['courses']:
            cursor.execute(
                '''
INSERT INTO tasks(step,type,task,status)
VALUES (?,?,?,?)
''',(step_no,'course',course,'pending'))
            
        for oncert in i['online_certifications']:
            cursor.execute(
                '''
INSERT INTO tasks(step,type,task,status)
VALUES (?,?,?,?)
''',(step_no,'online_certification',oncert,'pending'))
            
        for project in i['projects']:
            cursor.execute(
                '''
INSERT INTO tasks(step,type,task,status)
VALUES (?,?,?,?)
''',(step_no,'project',project,'pending'))

try:
    app=Flask(__name__)
    @app.route('/',methods=['GET','POST'])
    def template():
        if request.method=='POST':
            name=request.form['inp']    
            global response
            response=llm(name)
           
            print(response)
            #db_store(response)
        
            return render_template('index.html',l=json.loads(response),s=json.loads(response))
        else:
            return render_template('index.html',l=response,s=response)
        
    app.run(debug=True)


except Exception as e:
    print(e)

