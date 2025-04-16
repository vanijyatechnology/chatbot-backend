import PyPDF2

def parse_pdf(filepath):
    content = ""
    with open(filepath, "rb") as f:
        reader = PyPDF2.PdfReader(f)
        for page in reader.pages:
            content += page.extract_text() or ""
    return content.strip()
