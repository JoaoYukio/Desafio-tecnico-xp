import streamlit as st
from PIL import Image
import easyocr
import numpy as np

reader = easyocr.Reader(["pt", "en"])


def img_to_text(img: Image.Image) -> str:
    """
    Extrai texto de uma imagem usando OCR.

    Parâmetros:
    - img (PIL.Image.Image): A imagem da qual o texto deve ser extraído.

    Retorna:
    - str: O texto extraído da imagem.
    """
    img_np = np.array(img)
    result = reader.readtext(img_np, detail=0, paragraph=True)

    return result
