import PyPDF2


def read_pdf(file) -> str:
    """Lê o conteúdo do arquivo PDF e retorna o seu texto."""
    pdf_reader = PyPDF2.PdfReader(file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text
