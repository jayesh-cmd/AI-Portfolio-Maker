import pdfplumber

def extract_text_from_pdf(cvpath):
    all_text = ""
    with pdfplumber.open(cvpath) as pdf:
        for page_num , page in enumerate(pdf.pages):
            text = page.extract_text()
            if text:
               all_text += f"\n-------PAGE - {page_num+1}---------\n\n{text}"
    return all_text

path = r"C:\Users\Lenovo\OneDrive\Desktop\CV PROJECTS\Ai_Portfolio_Maker\Resume.pdf"
resume_text = extract_text_from_pdf(path)
with open("file.txt", "w", encoding="utf-8") as file:
    file.write(resume_text)

print("Text Extracted From PDF - SUCCESSFULLY")