import streamlit as st
from PyPDF2 import PdfReader


class PDF:
    def __init__(self, pdf: PdfReader):
        self.pdf = pdf

    def get_text(self) -> str:
        text = ""
        for page in self.pdf.pages:
            text += page.extractText()
        return text


def main():
    st.set_page_config(page_title="Desafio Técnico XP", layout="wide")

    pdfs = []

    b = st.chat_input("Digite o que deseja pesquisar.")

    if b:
        for pdf in pdfs:
            text = pdf.get_text()
            st.write(text)

    with st.sidebar:
        st.subheader("Ferramentas")
        databases = ["Pinecone", "Crhoma"]

        with st.expander("Upload de arquivos", expanded=False):
            pdf_docs = st.file_uploader(
                "Carregar documentos", type=["pdf"], accept_multiple_files=True
            )
            if st.button("Carregar"):
                with st.spinner("Processando dados..."):
                    for pdf in pdf_docs:
                        pdfs.append(PDF(PdfReader(pdf)))

        radio = st.sidebar.radio("Databases", databases)
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


if __name__ == "__main__":
    main()
