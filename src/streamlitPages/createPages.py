import streamlit as st
from streamlit_option_menu import option_menu
from langchain.embeddings import OpenAIEmbeddings
from dotenv import load_dotenv

from markdownText.databaseMarkdown import MARKDOWN as databaseMarkdown

from utils.pdfReader import read_pdf

from patterns.database import *

load_dotenv()

if st.session_state.get("db") == None:
    st.session_state.db = None


def create_chat_page():
    st.session_state.tabs = ["Chat"]

    menu = option_menu(
        menu_title=None,
        options=st.session_state.tabs,
    )

    if menu == "Chat":
        b = st.chat_input("Digite o que deseja pesquisar.")
        if st.session_state.db != None:
            if b:
                st.write(st.session_state.db.query(b))

    # if st.button("Add"):
    #     st.session_state.tabs.append("New Tab")
    #     st.session_state.tabs = list(set(st.session_state.tabs))
    #     st.experimental_rerun()

    with st.sidebar:
        st.subheader("Ferramentas")

        with st.expander("Upload de arquivos", expanded=False):
            pdf_doc = st.file_uploader(
                "Carregar documentos",
                type=["pdf"],
                accept_multiple_files=False,
            )
            if st.button("Carregar"):
                with st.spinner("Processando dados..."):
                    if st.session_state.db != None:
                        text = read_pdf(pdf_doc)
                        st.session_state.db.connect_fromText(text)
                    else:
                        st.error("Por favor, conecte-se a um banco de dados primeiro.")
                    # st.write(text)
                st.success("Documento carregado com sucesso!")


def create_config_page():
    databases = ["Pinecone", "Chroma"]
    radio = st.radio("Databases", databases, help=databaseMarkdown)

    if radio == "Pinecone":
        with st.expander("Configurações Pinecone", expanded=True):
            with st.form(key="my_form"):
                # cols = st.columns(3)
                # with cols[0]:
                #     api_key = st.text_input("Pinecone API Key")
                # with cols[1]:
                #     index = st.text_input("Pinecone Index")
                # with cols[2]:
                #     environment = st.text_input("Pinecone Environment")

                api_key = st.text_input("Pinecone API Key")
                index = st.text_input("Pinecone Index")
                environment = st.text_input("Pinecone Environment")
                if st.form_submit_button("Salvar"):
                    if not api_key or not index or not environment:
                        st.warning(
                            "Por favor, preencha todos os campos antes de enviar."
                        )
                    else:
                        st.success("Configurações enviadas com sucesso!")
    elif radio == "Chroma":
        directory = "./data"
        db_type = "chroma"
        embeddings = OpenAIEmbeddings()
        persist_directory = "./data/chroma_store"

        db = DatabaseFactory.create_database(
            database_type=db_type,
            embeddings=embeddings,
            persist_directory=persist_directory,
        )

        st.session_state.db = db
