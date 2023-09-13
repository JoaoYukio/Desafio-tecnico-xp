import PyPDF2
import os


def read_pdf(file) -> str:
    """Lê o conteúdo do arquivo PDF e retorna o seu texto."""
    if not file:
        raise ValueError("O arquivo PDF fornecido é inválido.")
    pdf_reader = PyPDF2.PdfReader(file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text


def save_pdf_to_folder(file, folder) -> str:
    if not file:
        raise ValueError("O arquivo PDF fornecido é inválido.")

    if not os.path.exists(folder):
        os.makedirs(folder)

    file_path = os.path.join(folder, file.name)

    with open(file_path, "wb") as f:
        f.write(file.getvalue())

    return file_path
