from langchain.chat_models import ChatOpenAI
from langchain.document_loaders import PyPDFLoader
from langchain.chains.summarize import load_summarize_chain


def summarize(path: str, llm: ChatOpenAI) -> str:
    loader = PyPDFLoader(path)
    pages = loader.load_and_split()
    chain = load_summarize_chain(llm, chain_type="stuff")
    summary = chain.run(pages)
    return summary
