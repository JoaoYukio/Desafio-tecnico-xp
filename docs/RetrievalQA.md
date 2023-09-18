# Retrieval Augmented Generation com LangChain

O processo de "Retrieval Augmented Generation" (Geração Aprimorada por Recuperação) tem ganhado destaque desde o lançamento do ChatGPT. A principal ideia é, em vez de simplesmente passar uma pergunta do usuário diretamente para um modelo de linguagem, o sistema "recupera" quaisquer documentos que possam ser relevantes para responder à pergunta e, em seguida, passa esses documentos (juntamente com a pergunta original) para o modelo de linguagem para uma etapa de "geração".

## Abordagem Semântica

A principal maneira pela qual a maioria das pessoas - incluindo a LangChain - tem feito a recuperação é usando busca semântica. Nesse processo, um vetor numérico (um embedding) é calculado para todos os documentos, e esses vetores são armazenados em um banco de dados vetorial. As consultas recebidas são então vetorizadas da mesma forma, e os documentos recuperados são aqueles que estão mais próximos da consulta no espaço de embedding. Para uma compreensão mais aprofundada sobre isso, confira [este tutorial](https://blog.langchain.dev/tutorial-chatgpt-over-your-data/).

![Busca Semântica]()

![Diagrama de etapa típica de recuperação](https://blog.langchain.dev/retrieval/diagram.png)

## Problemas e Soluções

A LangChain identificou algumas limitações em suas abstrações iniciais e fez ajustes para tornar mais fácil a utilização de outros métodos de recuperação além do objeto LangChain VectorDB. A ideia é permitir que os recuperadores construídos em outros lugares sejam usados mais facilmente na LangChain e incentivar mais experimentação com métodos alternativos de recuperação.

### Interface do Retriever

A LangChain introduziu o conceito de um Retriever, que é esperado para expor um método `get_relevant_documents` com a seguinte assinatura: `def get_relevant_documents(self, query: str) -> List[Document]`. Essa é a única suposição feita sobre os Retrievers.

Para mais detalhes e informações avançadas sobre RetrievalQA e como ele funciona com um banco de dados vetorial, consulte a [documentação oficial da LangChain](https://blog.langchain.dev/retrieval/).
