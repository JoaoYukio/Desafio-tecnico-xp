import PyPDF2


def read_pdf(file) -> str:
    """Lê o conteúdo do arquivo PDF e retorna o seu texto."""
    if not file:
        raise ValueError("O arquivo PDF fornecido é inválido.")
    pdf_reader = PyPDF2.PdfReader(file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text
