from langchain_core.prompts import PromptTemplate

start=PromptTemplate(template='Generate a roadmap for the user query {query}',input_variable=['query'])

course_suggestion=PromptTemplate(template="Considering this roadmap, suggest relevant and important courses "
        "in **valid JSON format only**, with keys 'courses' as a list of strings.\n"
        "Roadmap: {roadmap}",input_variables=['roadmap'])

online_certification=PromptTemplate(template="Considering this roadmap, suggest relevant and important online cerifications "
        "in **valid JSON format only**, with keys 'online certifications' as a list of strings.\n"
        "Roadmap: {roadmap}",input_variables=['roadmap'])

projects=PromptTemplate(template="Considering this roadmap, suggest relevant and important projects to build "
        "in **valid JSON format only**, with keys 'courses' as a list of strings.\n"
        "Roadmap: {roadmap}",input_variables=['roadmap'])

final=PromptTemplate(template='''You are given a roadmap and related learning resources.
Your task is to merge them into a **step-by-step JSON**.
The JSON must be an array of steps, where each step has these keys:
- "step_number": integer
- "description": string (brief explanation of the step)
- "courses": list of strings
- "online_certifications": list of strings
- "projects": list of strings

Use only **valid JSON** — no markdown code fences or extra text.

Roadmap:
{roadmap}

Courses:
{courses}

Projects:
{projects}

Online Certifications:
{online_certifications}

Return only the JSON array.
''',
input_variables=['roadmap','courses','projects','online_certifications'])

