# Script to make Portfolio site it will give you the index.html file

import json
import os
from jinja2 import FileSystemLoader , Environment

# Paste the path of json file here ----
path = r"Ai_Portfolio_Maker\traditional-extraction\Extracted_Info.json"
with open(path , "r") as f:
    data = json.load(f)

temp_path = r"Ai_Portfolio_Maker\templates"
env = Environment(loader = FileSystemLoader(temp_path))

html_template = env.get_template("Portfolio.html.j2")

html_output = html_template.render(**data)

os.makedirs("Here's_Your_Portfolio_Duh" , exist_ok=True)

with open("Here's_Your_Portfolio_Duh/Your_Portfolio.html" , "w" , encoding= "utf-8") as f:
    f.write(html_output)

print("✅ Portfolio website generated successfully!")
