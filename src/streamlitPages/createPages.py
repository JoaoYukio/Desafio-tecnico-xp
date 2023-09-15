import streamlit as st
from streamlit_option_menu import option_menu
from langchain.embeddings import OpenAIEmbeddings
from dotenv import load_dotenv

from langchain.llms import OpenAI
from langchain.chains import RetrievalQA

from markdownText.databaseMarkdown import MARKDOWN as databaseMarkdown
from markdownText.RCIMarkdown import MARKDOWN as RCIMarkdown

from utils.pdfReader import read_pdf, save_pdf_to_folder
from utils.summarize import summarize
from agents.wikipedia_agent import lookup

from langchain.document_loaders import PyPDFLoader
from PyPDF2 import PdfReader

from utils.saveJson import load_uploaded_files, save_uploaded_files

from chains.RCIChain import chain_RCI

# from utils.ocr import img_to_text
# from PIL import Image

from patterns.database import *
import os, tempfile

load_dotenv()


def create_chat_page():
    if "db" not in st.session_state:
        print("DB nao criado")
        st.session_state.db = None

    st.session_state.uploaded_files = load_uploaded_files()

    b = st.chat_input("Digite o que deseja pesquisar.")
    if st.session_state.db.get_vector_store() != None:
        if b:
            qa = RetrievalQA.from_chain_type(
                llm=OpenAI(temperature=0.3),
                chain_type="stuff",
                retriever=st.session_state.db.get_vector_store().as_retriever(),
                return_source_documents=True,
            )
            # st.write(st.session_state.db.query(b))

            res = qa({"query": b})

            #! TODO: Adicionar quais textos foram feito upload e criar um template para perguntar coisas especificas
            #! TODO: Adicionar memory
            st.write(res)
    else:
        st.warning("Por favor, carregue um banco de dados antes de pesquisar.")

    with st.expander("Conversar com um documento em específico", expanded=False):
        qSelect = st.selectbox(
            "Selecione um documento",
            [doc["filename"] for doc in st.session_state.uploaded_files],
        )
        bQuestions = st.button(
            "Insights sobre o documento gerados usando RCI", help=RCIMarkdown
        )
        if bQuestions:
            if qSelect:
                qText = [
                    doc["summary"]
                    for doc in st.session_state.uploaded_files
                    if doc["filename"] == qSelect
                ][0]

                # q = lookup(
                #     llm=OpenAI(temperature=0.3),
                #     num_perguntas=3,
                #     text=qText,
                # )

                q = chain_RCI(qText)

                st.write(q)
    sButton = st.button("Mostrar DB")
    if sButton:
        st.write(st.session_state.db.get_vectors())

    with st.sidebar:
        st.subheader("Ferramentas")

        with st.expander("Upload de arquivos", expanded=False):
            pdf_doc = st.file_uploader(
                "Carregar documentos",
                type=["pdf"],
                accept_multiple_files=False,
            )
            cols = st.columns(3)
            with cols[0]:
                bLoad = st.button("Salvar no DB")
            with cols[1]:
                bSave = st.button("Salvar")
            with cols[2]:
                bResume = st.button("Resumir")
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
                        # text = read_pdf(pdf_doc)
                        with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
                            tmp_file.write(pdf_doc.read())

                        loader = PyPDFLoader(tmp_file.name)
                        pages = loader.load_and_split()

                        file_info = {
                            "filename": pdf_doc.name,
                            "title": pdf_doc.name,
                            "summary": summarize(
                                tmp_file.name, llm=OpenAI(temperature=0.3)
                            ),
                            "file_size": pdf_doc.size,
                            "file_type": pdf_doc.type,
                            "path": tmp_file.name,
                        }

                        st.session_state.uploaded_files.append(file_info)
                        save_uploaded_files(st.session_state.uploaded_files)

                        st.success(f"Upload de {pdf_doc.name} concluído com sucesso!")

                        os.remove(tmp_file.name)

                    except ValueError:
                        st.error("Por favor, selecione um arquivo PDF válido.")
                        return
                    st.session_state.db.connect_fromDoc(pages)
                    st.success("Banco criado com sucesso!")

            if bResume:
                with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
                    tmp_file.write(pdf_doc.read())
                st.write(
                    summarize(
                        tmp_file.name,
                        llm=OpenAI(temperature=0.3),
                    )
                )

        with st.expander("Upload de imagens", expanded=False):
            uploaded_file = st.file_uploader(
                "Escolha uma imagem", type=["jpg", "jpeg", "png"]
            )
            # if uploaded_file:
            #     # Abre a imagem usando PIL
            #     img = Image.open(uploaded_file)

            #     # Mostra a imagem no Streamlit
            #     st.image(img, caption="Imagem carregada.", use_column_width=True)

            #     # Extrai texto usando OCR
            #     extracted_text = img_to_text(img)

            #     # Mostra o texto extraído
            #     st.write("Texto extraído:")
            #     st.write(extracted_text)

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
