import pdfplumber
import json
import os
from jinja2 import FileSystemLoader , Environment
from langchain_ollama import OllamaLLM
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import PromptTemplate
from pydantic import BaseModel, Field
import json

# First we have to extract text from the PDF so we can give the text to LLM Directly
def extract_text_from_pdf(cvpath):
    all_text = ""
    with pdfplumber.open(cvpath) as pdf:
        for page_num , page in enumerate(pdf.pages):
            text = page.extract_text()
            if text:
               all_text += f"\n-------PAGE - {page_num+1}---------\n\n{text}"
    return all_text

path = r"C:\Users\Lenovo\OneDrive\Desktop\Harry Python\Updated AI Resume\Jayesh Vishwakarma Resume AIML.pdf"

resume_text = extract_text_from_pdf(path)


# Extract Info From The Text And Generate Json Output --

# TO USE THIS ITS NEED TO INSTALL OLLAMA, LLM(Model=""llama3.2:latest"") AND LANGCHAIN
model = OllamaLLM(model="llama3.2:latest") # Here i used llama3.2 model locally , You can use API

# Text File Import , So we can give it to llm for info extraction

class ProjectItem(BaseModel):
    title: str
    items: list[str]

class EducationItem(BaseModel):
    description: str
    title: str
    courseWork: list[str]

class extract_info(BaseModel):

    Name : str = Field(description="extract full name from this resume")
    Email : str = Field(description="from the given resume extract email")
    Phone : str = Field(description="from the resume ectract the phone number")
    Skills : list[str] =Field(description="from the resume ectract skills")
    Projects : list[ProjectItem] = Field(description="List of projects with titles and details")
    Education : EducationItem = Field(description="Education details with description, title and coursework")

parser = PydanticOutputParser(pydantic_object=extract_info)

# Chat Template
template = PromptTemplate(
    template="""Extract the following information from the resume:
    - Name
    - Email
    - Phone
    - Skills (as list)
    - Projects (with title and items list for each)
    - Education (with description, title and coursework)
    
    Format as valid JSON matching the schema.
    
    Resume: {text}
    {format_instruction}""",
    input_variables=['text'],
    partial_variables={'format_instruction': parser.get_format_instructions()}
)

chain = template | model | parser

result = chain.invoke({'text':resume_text})

# Script to make Portfolio site it will give you the index.html file
# Paste the path of json file here ----

temp_path = r"C:\Users\Lenovo\OneDrive\Desktop\Harry Python\Updated AI Resume\templates"
env = Environment(loader = FileSystemLoader(temp_path))

html_template = env.get_template("Portfolio.html.j2")

html_output = html_template.render(result.dict())

os.makedirs("Here's_Your_Portfolio_Duh" , exist_ok=True)

with open("Here's_Your_Portfolio_Duh/Your_Portfolio.html" , "w" , encoding= "utf-8") as f:
    f.write(html_output)

print("✅ Portfolio website generated successfully!")
