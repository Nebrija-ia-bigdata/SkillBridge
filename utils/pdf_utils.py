import fitz 

def extract_pdf_text(pdf_file):
    #Extrae el texto del PDF subido usando PyMuPDF.
    pdf_file.seek(0)
    pdf_bytes = pdf_file.read()
    document = fitz.open(stream=pdf_bytes, filetype="pdf")
    text = ""
    for page in document:
        text += page.get_text()
    return text
