# TO USE THIS ITS NEED TO INSTALL OLLAMA, LLM(Model=""llama3.2:latest"") AND LANGCHAIN

from langchain_ollama import OllamaLLM
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import PromptTemplate
from pydantic import BaseModel, Field
import json

model = OllamaLLM(model="llama3.2:latest") # Here i used llama3.2 model locally , You can use API

# Text File Import , So we can give it to llm for info extraction
txt_path = r"C:\Users\Lenovo\OneDrive\Desktop\Harry Python\CV PROJECTS\Ai_Portfolio_Maker\CV_EXTRACTED_INFO.txt" # Text File Path
with open(txt_path, "r") as f:
    file = f.read()

# Define Structure

class ProjectItem(BaseModel):
    title: str
    items: list[str]

class EducationItem(BaseModel):
    description: str
    title: str
    courseWork: list[str]

class extract_info(BaseModel):

    Name : str = Field(description="extract full name from this resume"),
    Email : str = Field(description="from the given resume extract email"),
    Phone : str = Field(description="from the resume ectract the phone number"),
    Skills : list[str] =Field(description="from the resume ectract skills"),
    Projects : list[ProjectItem] = Field(description="List of projects with titles and details"),
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

result = chain.invoke({'text':file})
json_output = json.dumps(result.model_dump(), indent=2)

with open('Extracted_Info.json', 'w') as f:
    f.write(json_output)

print("Extracted Info Saved Successfully As JSON ")