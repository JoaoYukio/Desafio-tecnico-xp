# Desafio-tecnico-xp

Este repositório contém o projeto desenvolvido como parte de um desafio proposto. A aplicação é construída utilizando o framework LangChain para interação com modelos de linguagem e Streamlit para a interface do usuário.

## 📌 Índice

-   [Pré-requisitos](#-pré-requisitos)
-   [Instalação](#-instalação)
-   [Uso](#-uso)
-   [Documentações Adicionais](#-documentações-adicionais)
-   [Licença](#-licença)

## 🛠 Pré-requisitos

Antes de começar, certifique-se de ter as seguintes ferramentas instaladas em sua máquina:

-   **Python**: A linguagem de programação principal usada neste projeto.

    -   [Download Python](https://www.python.org/downloads/)

-   **Pipenv**: Uma ferramenta de gerenciamento de dependências e ambiente virtual para Python.

    -   Instalação:
        ```bash
        pip install pipenv
        ```

-   **Docker**: Uma plataforma para desenvolver, enviar e executar aplicações em containers.

    -   [Download Docker](https://www.docker.com/products/docker-desktop)

-   **Git**: Uma ferramenta de controle de versão distribuído usada para rastrear mudanças no código fonte durante o desenvolvimento de software.
    -   [Download Git](https://git-scm.com/downloads)

## 🚀 Instalação

Para configurar e executar o projeto usando Docker, siga os passos abaixo:

### Clonando o Repositório

Primeiro, clone o repositório para sua máquina local:

```bash
git clone https://github.com/JoaoYukio/Desafio-tecnico-xp.git
cd Desafio-tecnico-xp
```

### Usando Docker

Construa a imagem Docker e execute o container:

```bash
docker build -t desafio-tecnico-xp .
docker run -p 8080:8080 desafio-tecnico-xp
```

Após executar o container, acesse a aplicação em http://localhost:8080.

## 🖥 Uso

O aplicativo oferece uma interface intuitiva que permite aos usuários interagir com documentos e obter insights valiosos. Aqui estão as principais funcionalidades:

### Upload de Arquivos

-   **Armazenamento no Chroma**: Você pode fazer upload de arquivos que serão armazenados em um banco de dados Chroma. Isso facilita a organização, recuperação e análise de documentos.

### Geração de Insights

-   **Insights de Documentos Individuais**: Na parte superior do chat, você pode gerar insights de documentos individuais. Isso permite uma análise rápida e compreensão do conteúdo do documento.

### Perguntas e Respostas

-   **Busca Contextual (Retrieval Augmented Generation)**: Você pode fazer perguntas gerais no chat. O sistema tentará buscar nos documentos armazenados para fornecer uma resposta contextualizada. Esta funcionalidade utiliza a técnica de Retrieval Augmented Generation para obter um contexto da sua pergunta e fornecer respostas mais precisas.

### Uso de Agentes

-   **Agente da LangChain**: O aplicativo também oferece a possibilidade de usar um [agente da LangChain](https://docs.langchain.com/docs/components/agents/) para fazer buscas e obter insights e resumos. Este agente utiliza os dados disponíveis na Wikipedia para fornecer informações ricas e contextualizadas.

## 📚 Documentações Adicionais

-   [RCI Chain](./docs/rci_chain.md): Saiba mais sobre como o RCI Chain foi utilizado neste projeto.
-   [RetrievalQA](./docs/RetrievalQA.md): Informações detalhadas sobre RetrievalQA.
-   [Agents](./docs/agents.md): Informações detalhadas sobre agentes.
