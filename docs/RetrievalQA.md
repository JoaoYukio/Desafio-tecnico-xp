# Retrieval Augmented Generation com LangChain

O processo de "Retrieval Augmented Generation" (Geração Aprimorada por Recuperação) tem ganhado destaque desde o lançamento do ChatGPT. A principal ideia é, em vez de simplesmente passar uma pergunta do usuário diretamente para um modelo de linguagem, o sistema "recupera" quaisquer documentos que possam ser relevantes para responder à pergunta e, em seguida, passa esses documentos (juntamente com a pergunta original) para o modelo de linguagem para uma etapa de "geração".

![Diagrama de etapa típica de recuperação](https://github.com/JoaoYukio/Desafio-tecnico-xp/blob/638d62f5d8abf8061c70e126f3b589f185e7bd56/docs/imgs/retrieval.png)

## Abordagem Semântica

A principal maneira pela qual a maioria das pessoas - incluindo a LangChain - tem feito a recuperação é usando busca semântica. Nesse processo, um vetor numérico (um embedding) é calculado para todos os documentos, e esses vetores são armazenados em um banco de dados vetorial. As consultas recebidas são então vetorizadas da mesma forma, e os documentos recuperados são aqueles que estão mais próximos da consulta no espaço de embedding. Para uma compreensão mais aprofundada sobre isso, confira [este tutorial](https://blog.langchain.dev/tutorial-chatgpt-over-your-data/).

![Busca Semântica](https://github.com/JoaoYukio/Desafio-tecnico-xp/blob/638d62f5d8abf8061c70e126f3b589f185e7bd56/docs/imgs/semantic_search.png)

## Informações Extras

Para mais detalhes e informações avançadas sobre RetrievalQA e como ele funciona com um banco de dados vetorial, consulte a [documentação oficial da LangChain](https://blog.langchain.dev/retrieval/).
