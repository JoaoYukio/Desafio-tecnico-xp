from abc import ABC, abstractmethod

from langchain.vectorstores import Chroma
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import (
    CharacterTextSplitter,
    RecursiveCharacterTextSplitter,
)
from langchain.docstore.document import Document

from langchain.document_loaders import DirectoryLoader


class DatabaseInterface(ABC):
    @abstractmethod
    def connect_fromDoc(self, docs: list):
        pass

    @abstractmethod
    def connect_fromText(self, text: str):
        pass

    @abstractmethod
    def query(self, query_string: str):
        pass

    @abstractmethod
    def load_documents(self, directory: str) -> Document:
        pass

    @abstractmethod
    def doc_splitter(self, documents: str, chunk_size: int, chunk_overlap: int) -> list:
        pass

    @abstractmethod
    def text_splitter(self, text: str, chunk_size: int, chunk_overlap: int) -> list:
        pass

    @abstractmethod
    def append_documents(self, documents: list):
        pass

    @abstractmethod
    def append_text(self, text: str):
        pass


class ChromaDatabase(DatabaseInterface):
    def __init__(self, embeddings: OpenAIEmbeddings, persist_directory: str):
        self.embeddings = embeddings
        self.persist_directory = persist_directory
        self.docsearch = None

    def load_documents(self, directory: str) -> Document:
        return DirectoryLoader(directory).load()

    def load_text(self, directory: str) -> str:
        return DirectoryLoader(directory).load_text()

    def doc_splitter(self, documents: str, chunk_size=1000, chunk_overlap=20) -> list:
        return RecursiveCharacterTextSplitter(
            chunk_size=chunk_size, chunk_overlap=chunk_overlap
        ).split_documents(documents)

    def text_splitter(self, text: str, chunk_size=1000, chunk_overlap=20) -> list:
        return RecursiveCharacterTextSplitter(
            chunk_size=chunk_size, chunk_overlap=chunk_overlap
        ).split_text(text)

    def connect_fromDoc(self, docs: list):
        if not self.docsearch:
            self.docsearch = Chroma.from_documents(
                documents=self.text_splitter(docs),
                embedding=self.embeddings,
                persist_directory=self.persist_directory,
            )
            self.docsearch.persist()

    def connect_fromText(self, text: str):
        if not self.docsearch:
            self.docsearch = Chroma.from_texts(
                texts=self.text_splitter(text),
                embedding=self.embeddings,
                persist_directory=self.persist_directory,
            )
            self.docsearch.persist()

    def append_documents(self, documents: list) -> None:
        if not self.docsearch:
            print("Erro: Banco de dados Chroma não está conectado.")
            return
        self.docsearch.add_documents(documents=documents)

    def append_text(self, text: str) -> None:
        if not self.docsearch:
            print("Erro: Banco de dados Chroma não está conectado.")
            return
        self.docsearch.add_texts(texts=text)

    def query(self, query_string: str) -> list:
        if self.docsearch:
            return self.docsearch.similarity_search(query_string, k=5)
        else:
            print("Erro: Banco de dados Chroma não está conectado.")
            return []


class DatabaseFactory:
    @staticmethod
    def create_database(database_type: str, **kwargs) -> DatabaseInterface:
        """
        Cria uma instância de banco de dados com base no tipo fornecido.

        :param database_type: Tipo do banco de dados ('chroma', 'pinecone', etc.)
        :param kwargs: Argumentos adicionais necessários para inicializar o banco de dados.
        :return: Uma instância do banco de dados.
        """
        if database_type == "chroma":
            embeddings = kwargs.get("embeddings", OpenAIEmbeddings())
            persist_directory = kwargs.get("persist_directory", "chroma_store")
            return ChromaDatabase(
                embeddings=embeddings, persist_directory=persist_directory
            )

        # elif database_type == 'pinecone':
        #     return PineconeDatabase(**kwargs)

        else:
            raise ValueError(f"Tipo de banco de dados '{database_type}' não suportado.")
