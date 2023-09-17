import streamlit as st
from streamlit_option_menu import option_menu
from langchain.embeddings import OpenAIEmbeddings
from dotenv import load_dotenv

from langchain.llms import OpenAI
from langchain.chains import RetrievalQA

from markdownText.databaseMarkdown import MARKDOWN as databaseMarkdown
from markdownText.RCIMarkdown import MARKDOWN as RCIMarkdown
from markdownText.OpenAIKeyMarkdown import MARKDOWN as OpenAIKeyMarkdown

from utils.pdfReader import read_pdf, save_pdf_to_folder
from utils.summarize import summarize
from agents.wikipedia_agent import lookup
from utils.testOpenAIKey import is_api_key_valid

from langchain.document_loaders import PyPDFLoader
from PyPDF2 import PdfReader

from utils.saveJson import load_uploaded_files, save_uploaded_files

from chains.RCIChain import chain_RCI

# from utils.ocr import img_to_text
# from PIL import Image

from patterns.database import *
import os, tempfile

# load_dotenv()

OPENAI_API_KEY = st.session_state.get("OPENAI_API_KEY", "")


def create_chat_page():
    if "db" not in st.session_state:
        print("DB nao criado")
        st.session_state.db = None

    if "messages" not in st.session_state:
        st.session_state.messages = []

    st.session_state.uploaded_files = load_uploaded_files()

    b = st.chat_input("Digite o que deseja pesquisar.")
    if st.session_state.db.get_vector_store() != None:
        if b:
            qa = RetrievalQA.from_chain_type(
                llm=OpenAI(
                    temperature=0.3, openai_api_key=st.session_state["OPENAI_API_KEY"]
                ),
                chain_type="stuff",
                retriever=st.session_state.db.get_vector_store().as_retriever(),
                return_source_documents=True,
            )
            # st.write(st.session_state.db.query(b))

            res = qa({"query": b})

            #! TODO: Adicionar quais textos foram feito upload e criar um template para perguntar coisas especificas
            #! TODO: Adicionar memory
            with st.chat_message("user"):
                st.markdown(b)

            with st.chat_message("assistant"):
                # st.write(res)
                st.write(res["result"])
                with st.expander("Documentos relevantes", expanded=False):
                    for doc in res["source_documents"]:
                        st.write(doc)

            st.session_state.messages.append({"role": "user", "content": b})
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

                q = chain_RCI(qText, st.session_state["OPEN_API_KEY"])

                with st.chat_message("assistant"):
                    st.write(q)
    # sButton = st.button("Mostrar DB")
    # if sButton:
    #     st.write(st.session_state.db.get_vectors())

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
                bResume = st.button("Resumir")

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
                                tmp_file.name,
                                llm=OpenAI(
                                    temperature=0.3,
                                    openai_api_key=st.session_state["OPENAI_API_KEY"],
                                ),
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
                        llm=OpenAI(
                            temperature=0.3,
                            openai_api_key=st.session_state["OPENAI_API_KEY"],
                        ),
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


def set_open_api_key(api_key: str) -> bool:
    if is_api_key_valid(api_key):
        st.session_state["OPENAI_API_KEY"] = api_key
        st.session_state["open_api_key_configured"] = True
        return True
    else:
        st.session_state["OPENAI_API_KEY"] = None
        st.session_state["open_api_key_configured"] = False
        return False


def create_config_page():
    st.markdown(OpenAIKeyMarkdown)
    open_api_key_input = st.text_input(
        "Openai API Key",
        type="password",
        placeholder="Cole sua chave de API aqui (sk-...)",
        help="Você pode obter sua chave de API em https://platform.openai.com/account/api-keys.",  # noqa: E501
        value=st.session_state.get("OPENAI_API_KEY", ""),
    )

    if open_api_key_input:
        if set_open_api_key(open_api_key_input):
            st.success("Chave de API válida!")
        else:
            st.warning("Chave de API inválida.")

    if not st.session_state.get("open_api_key_configured"):
        st.error("Configure sua chave Open API!")
        st.session_state.db = None

    else:
        st.markdown("Chave de API aberta configurada!")
        db_type = "chroma"
        embeddings = OpenAIEmbeddings(openai_api_key=st.session_state["OPENAI_API_KEY"])
        persist_directory = "/app/src/data/chroma_store/"

        db = DatabaseFactory.create_database(
            database_type=db_type,
            embeddings=embeddings,
            persist_directory=persist_directory,
        )

        st.session_state.db = db
