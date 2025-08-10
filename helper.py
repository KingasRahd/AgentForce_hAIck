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

response='sdfghj'
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
           # response=llm(name)
            response='''
[
  {
    "step_number": 1,
    "description": "Get a foundational understanding of what a car is, its main components, and how it generally works. Identify main parts, their basic functions, different car types, and fundamental terminology.",
    "courses": [
      "Introduction to Automotive Systems"
    ],
    "online_certifications": [
      "Automotive Basics Certification (Udemy)"
    ],
    "projects": [
      "Introduction to Automotive Components: Identify and Understand Basic Car Parts",
      "How Car Systems Work: A Beginner's Guide to Powertrain, Chassis, and Brakes",
      "Understanding Different Car Types: Sedans, SUVs, EVs, and More",
      "Automotive Terminology Explained: Horsepower, Torque, MPG, and Drivetrains"
    ]
  },
  {
    "step_number": 2,
    "description": "Understand how the major systems of a car work together, including the powertrain (engine, transmission, drivetrain), chassis and suspension, braking system, steering system, and basic electrical system.",
    "courses": [
      "Understanding Internal Combustion Engines",
      "Automotive Drivetrain Components",
      "Suspension and Steering Systems",
      "Braking Systems: Theory and Practice",
      "Automotive Electrical Systems Fundamentals"
    ],
    "online_certifications": [
      "Introduction to Automotive Systems (Coursera/edX)",
      "Automotive Electrical Systems (Udemy)",
      "Brake Systems Service (Online Training Modules)",
      "Suspension and Steering Systems (Online Training Modules)",
      "Basic Engine Repair (Online Courses)"
    ],
    "projects": [
      "Deep Dive into the Powertrain: Engine, Transmission, and Drivetrain Mechanics",
      "The Science of Suspension and Chassis: Ride Comfort and Handling Explained",
      "Braking Systems 101: How to Stop Safely",
      "Fundamentals of Automotive Electrical Systems: Battery, Alternator, and Starter"
    ]
  },
  {
    "step_number": 3,
    "description": "Gain practical knowledge about maintaining and understanding your car's needs. Focus on the owner's manual, basic maintenance tasks, dashboard warning lights, and basic troubleshooting.",
    "courses": [
      "Basic Car Maintenance and Repair",
      "Car Care and Detailing"
    ],
    "online_certifications": [
      "Automotive Maintenance and Repair Fundamentals (Udemy)",
      "Car Diagnostics and Troubleshooting (Udemy)",
      "Hybrid Vehicle Technology (Online Courses)"
    ],
    "projects": [
      "Your Car's Owner's Manual: A Practical Guide to Maintenance and Care",
      "Essential Car Maintenance Tasks: Fluids, Tires, Filters, and Wiper Blades",
      "Decoding Dashboard Warning Lights: What Your Car is Trying to Tell You",
      "Basic Automotive Troubleshooting: Common Issues and Solutions",
      "Car Care and Detailing: Keeping Your Vehicle Pristine"
    ]
  },
  {
    "step_number": 4,
    "description": "Understand more complex systems, performance aspects, and how to diagnose and potentially fix more involved issues. This includes detailed engine components, advanced transmission types, electrical/electronic systems, suspension, braking, EVs/hybrids, and diagnostic tools.",
    "courses": [
      "Advanced Automotive Engine Diagnostics",
      "Vehicle Dynamics and Performance",
      "Electric and Hybrid Vehicle Technology",
      "Automotive Diagnostic Tools and Techniques"
    ],
    "online_certifications": [
      "Understanding Electric Vehicles (EV) Technology (Coursera)",
      "Automotive Diagnostic Tools and Techniques (Udemy)"
    ],
    "projects": [
      "Advanced Engine Systems: Turbochargers, Cooling, and Lubrication",
      "Transmission Technologies: CVTs, DCTs, and Torque Converters",
      "Automotive Electronics and Diagnostics: ECUs, Sensors, and CAN Bus",
      "Performance Suspension and Handling: Tuning for the Road",
      "In-Depth Braking Systems: Disc vs. Drum, Bleeding, and Upgrades",
      "Electric and Hybrid Vehicle Technology: Battery, Charging, and Regenerative Braking",
      "Using OBD-II Scanners: Reading Codes and Basic Diagnostics"
    ]
  }
]
'''
            return render_template('index.html',l=json.loads(response))
        else:
            return render_template('index.html',l=response)
        
    app.run(debug=True)


except Exception as e:
    print(e)

