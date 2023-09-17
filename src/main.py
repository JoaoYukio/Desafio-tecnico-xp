import streamlit as st
from PyPDF2 import PdfReader
from streamlit_option_menu import option_menu

from streamlitPages.createPages import create_chat_page, create_config_page


def main():
    st.set_page_config(
        page_title="Desafio Técnico XP",
        layout="wide",
    )

    with st.sidebar:
        pageSelection = option_menu(
            menu_title=None,
            options=["Chat", "Configurações"],
            icons=["chat-dots", "gear"],
            manual_select=1,
        )
    if st.session_state.get("OPENAI_API_KEY", "") == "":
        if pageSelection == "Chat":
            st.warning("Por favor, configure a API antes de acessar o chat.")
            create_config_page()
        elif pageSelection == "Configurações":
            create_config_page()
    else:
        if pageSelection == "Chat":
            create_chat_page()
        elif pageSelection == "Configurações":
            create_config_page()


if __name__ == "__main__":
    main()
