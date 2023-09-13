import streamlit as st
from streamlit_option_menu import option_menu
from langchain.embeddings import OpenAIEmbeddings
from dotenv import load_dotenv

from langchain.llms import OpenAI
from langchain.chains import RetrievalQA

from markdownText.databaseMarkdown import MARKDOWN as databaseMarkdown

from utils.pdfReader import read_pdf, save_pdf_to_folder

from utils.ocr import img_to_text
from PIL import Image

from patterns.database import *
import os

load_dotenv()

if "db" not in st.session_state:
    print("DB nao criado")
    st.session_state.db = None


def create_chat_page():
    b = st.chat_input("Digite o que deseja pesquisar.")
    if st.session_state.db != None:
        if b:
            qa = RetrievalQA.from_chain_type(
                llm=OpenAI(temperature=0.3),
                chain_type="stuff",
                retriever=st.session_state.db.get_vector_store().as_retriever(),
            )
            # st.write(st.session_state.db.query(b))
            ##! TODO: Adicionar prompt engineering aqui

            res = qa({"query": b})

            #! TODO: Adicionar quais textos foram feito upload e criar um template para perguntar coisas especificas
            st.write(res)

    with st.sidebar:
        st.subheader("Ferramentas")

        with st.expander("Upload de arquivos", expanded=False):
            pdf_doc = st.file_uploader(
                "Carregar documentos",
                type=["pdf"],
                accept_multiple_files=False,
            )
            cols = st.columns(2)
            with cols[0]:
                bLoad = st.button("Salvar no DB")
            with cols[1]:
                bSave = st.button("Salvar")
            if bSave:
                if pdf_doc:
                    try:
                        saved_path = save_pdf_to_folder(pdf_doc, "./data/pdf_files/")
                        st.success(f"Arquivo salvo em: {saved_path}")
                    except ValueError as e:
                        st.error("Por favor, selecione um arquivo PDF válido.")
            if bLoad:
                with st.spinner("Processando dados..."):
                    try:
                        text = read_pdf(pdf_doc)
                    except ValueError:
                        st.error("Por favor, selecione um arquivo PDF válido.")
                        return
                    st.session_state.db.connect_fromText(text)
                    st.success("Banco criado com sucesso!")

        with st.expander("Upload de imagens", expanded=False):
            uploaded_file = st.file_uploader(
                "Escolha uma imagem", type=["jpg", "jpeg", "png"]
            )
            if uploaded_file:
                # Abre a imagem usando PIL
                img = Image.open(uploaded_file)

                # Mostra a imagem no Streamlit
                st.image(img, caption="Imagem carregada.", use_column_width=True)

                # Extrai texto usando OCR
                extracted_text = img_to_text(img)

                # Mostra o texto extraído
                st.write("Texto extraído:")
                st.write(extracted_text)

        with st.expander("Selecione os modelos", expanded=False):
            sModel = st.selectbox(
                "Modelo de linguagem", ["gpt-3.5-turbo", "Outros modelos"]
            )
            st.session_state.model = sModel


def create_config_page():
    databases = ["Pinecone", "Chroma"]
    radio = st.radio(
        "Databases",
        databases,
        help=databaseMarkdown,
        index=1,
    )

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
        persist_directory = "./data/chroma_store/"

        db = DatabaseFactory.create_database(
            database_type=db_type,
            embeddings=embeddings,
            persist_directory=persist_directory,
        )

        st.session_state.db = db
