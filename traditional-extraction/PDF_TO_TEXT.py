# First we have to extract text from the PDF so we can give the text to LLM Directly

import pdfplumber

def extract_text_from_pdf(cvpath):
    all_text = ""
    with pdfplumber.open(cvpath) as pdf:
        for page_num , page in enumerate(pdf.pages):
            text = page.extract_text()
            if text:
               all_text += f"\n-------PAGE - {page_num+1}---------\n\n{text}"
    return all_text

path = r"C:\Users\Lenovo\OneDrive\Desktop\Harry Python\CV PROJECTS\Ai_Portfolio_Maker\Jayesh Vishwakarma Resume AIML.pdf"
resume_text = extract_text_from_pdf(path)
with open("CV_EXTRACTED_INFO.txt", "w", encoding="utf-8") as file:
    file.write(resume_text)

print("Text Extracted From PDF - SUCCESSFULLY")