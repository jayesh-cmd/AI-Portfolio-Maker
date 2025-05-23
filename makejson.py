import spacy
import os
import json
import re
from spacy.pipeline import EntityRuler

file_text = r"C:\Users\Lenovo\OneDrive\Desktop\CV PROJECTS\file.txt"

with open(file_text, "r", encoding="utf-8") as file:
    resume_text = file.read()

def extract_name(resume_text):

    nlp = spacy.load("en_core_web_sm")
    ruler = nlp.add_pipe("entity_ruler", before="ner")

    patterns = [
        {"label": "PERSON", "pattern": [{"TEXT": {"REGEX": "^[A-Z][a-z]+$"}}, {"TEXT": {"REGEX": "^[A-Z][a-z]+$"}}]},
        {"label": "PERSON", "pattern": [{"TEXT": {"REGEX": "^[A-Z]{2,}$"}}, {"TEXT": {"REGEX": "^[A-Z]{2,}$"}}]},
    ]
    ruler.add_patterns(patterns)

    lines = resume_text.split("\n")
    top_text = "\n".join(lines[:5])
    doc = nlp(top_text)

    name = None

    for ent in doc.ents:
        if ent.label_ == 'PERSON' and not any(x in ent.text.lower() for x in ['school' , 'college' , 'institute']):
            name = ent.text.strip()
            print("Name Found By Entity : " , name)
            break
    
    if not name:
       first_line = lines[0].strip()
       if first_line.isupper() and 1< len(first_line.split()) <= 4:
           name = first_line.title()
           print("Name Found In First Line : " , name)

    if not name:
        email_match = re.findall(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", resume_text)
        if email_match:
            username = email_match[0].split("@")[0]
            username = re.sub(r"\d+","", username)
            if any(symbol in username for symbol in ['.' , '-' , '_']):
                parts = re.split(r'[._-]' , username)
                name = " ".join(part.capitalize() for part in parts if part)
                print("Name Found From Email : " , name)
    return name

extracted_name = extract_name(resume_text)

email = re.findall(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", resume_text)
phone = re.findall(r"\+?\d[\d\s\-()]{10,}\d", resume_text)
print(f"Email : {email} , Phone : {phone}")

with open(r'C:\Users\Lenovo\OneDrive\Desktop\CV PROJECTS\Ai_Portfolio_Maker\Skills.txt' , 'r') as f:
     skills_ihave = set(line.strip().lower() for line in f)

found_skills = [] # Stored All Skills From Resume
resume_lower = resume_text.lower()

for skill in skills_ihave:
    if skill in resume_lower:
        found_skills.append(skill)

# print("Skills Found:")
# for skill in found_skills:
#     print(f"- {skill}")

lines = resume_text.split("\n")

projects = []
for i in range(len(lines)):
        line = lines[i].strip()

        if "github.com" in line:
            match = re.match(r"^(.*?)(https?://github\.com/\S+)", line)
            if match:
                title = match.group(1).strip("-:\t")
                link = match.group(2).strip()
            else:
                continue
            
            if not title:
                title = link.rstrip("/").split("/")[-1].replace("-"," ").title()

            if i + 1 < len(lines):
                description = lines[i+1].strip()
            else:
                description = ""
            projects.append({
                "title" : title ,
                "link" : link ,
                "description" : description
            })

for proj in projects:
    print(f"\n{proj['title']}\n{proj['link']}\n{proj['description']} \n\n")

education = []
collect = False
edu_lines = []

for line in lines:
    line = line.strip()

    if "education" in line.lower().strip():
        collect = True
        continue
    if collect and("skills" in line.lower() or "projects" in line.lower()):
        break

    if collect and line:
        edu_lines.append(line)

import re

for i in range(0, len(edu_lines), 2):
    if i + 1 < len(edu_lines):
        institute = edu_lines[i]
        line = edu_lines[i+1]

        match = re.search(r"(.*?)(\d{4}\s*[-–to]+\s*\d{4})", line)
        if match:
            degree = match.group(1).strip()
            years = match.group(2).strip()
        else:
            degree = line
            years = ""

        education.append({
            "institute": institute,
            "degree": degree,
            "years": years
        })

print("Education Section:")
for edu in education:
    print(f"{edu['institute']} \n {edu['degree']} {edu['years']} \n\n")


parsed = {
    "Name" : extracted_name,
    "Email" : email[0] if email else None ,
    "Phone" : phone[0] if phone else None ,
    "Skills" : list(found_skills) ,
    "Projects" : projects,
    "Education" : education
}

with open('final.json' , 'w') as file:
    json.dump(parsed , file , indent=4)
print("File Saved Successfully")