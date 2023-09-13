import streamlit as st
from PIL import Image
import pytesseract


def img_to_text(img: Image.Image) -> str:
    """
    Extrai texto de uma imagem usando OCR.

    Parâmetros:
    - img (PIL.Image.Image): A imagem da qual o texto deve ser extraído.

    Retorna:
    - str: O texto extraído da imagem.
    """

    # Usa pytesseract para extrair texto
    text = pytesseract.image_to_string(img)

    return text
