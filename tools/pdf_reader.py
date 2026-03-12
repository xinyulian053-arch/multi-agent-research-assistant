import pdfplumber
import requests

def read_pdf_from_url(url):

    response = requests.get(url)

    with open("temp.pdf", "wb") as f:
        f.write(response.content)

    text = ""

    with pdfplumber.open("temp.pdf") as pdf:
        for page in pdf.pages:
            text += page.extract_text() or ""

    return text[:3000]