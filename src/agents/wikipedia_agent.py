from langchain.document_loaders import WikipediaLoader
from langchain import PromptTemplate
from langchain.agents import initialize_agent, Tool, AgentType


def search_wikipedia(query: str, load_max_docs: int = 1):
    docs = WikipediaLoader(query=query, load_max_docs=load_max_docs).load()
    if docs:
        return docs[0].page_content[:400]
    else:
        return "Nenhum documento encontrado."


def lookup(llm, num_perguntas: int, text: str) -> str:
    """
    Search for a topic in Wikipedia and return the first document.
    """
    template = """
    Gostaria que criasse {num_perguntas} perguntas interessantes sobre o texto {text} que você acabou de ler.
    """

    tools_for_agent = [
        Tool(
            name="Procurar na Wikipedia",
            func=search_wikipedia,
            description="Procura um tópico na Wikipedia e retorna o primeiro documento.",
        )
    ]

    agent = initialize_agent(
        tools=tools_for_agent,
        llm=llm,
        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True,
    )

    prompt_template = PromptTemplate(
        template=template, input_variables=["num_perguntas", "text"]
    )

    questions = agent.run(
        prompt_template.format_prompt(
            num_perguntas=num_perguntas,
            text=text,
        )
    )

    return questions
