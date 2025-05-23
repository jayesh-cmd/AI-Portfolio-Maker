import json
import os
from jinja2 import FileSystemLoader , Environment

path = r"C:\Users\Lenovo\OneDrive\Desktop\CV PROJECTS\final.json"
with open(path , "r") as f:
    data = json.load(f)

env = Environment(loader = FileSystemLoader(r"Ai_Portfolio_Maker\templates"))

html_template = env.get_template("portfolio.html.j2")

html_output = html_template.render(**data)

os.makedirs("output" , exist_ok=True)

with open("Output/index.html" , "w" , encoding= "utf-8") as f:
    f.write(html_output)

print("✅ Portfolio website generated successfully!")
