## 🤖 Agentes

Os agentes da LangChain são projetados para usar um LLM (Language Model) para escolher uma sequência de ações a serem realizadas. Em vez de ter uma sequência de ações pré-determinada, os agentes podem decidir dinamicamente quais ações tomar com base no input do usuário.

### Componentes Principais:

1. **Agente**: É a classe responsável por decidir o próximo passo a ser tomado. É alimentado por um modelo de linguagem e um prompt. Esse prompt pode incluir:

    - Personalidade do agente.
    - Contexto de fundo para o agente.
    - Estratégias de prompt para melhorar o raciocínio.

    A LangChain fornece vários tipos de agentes para começar, mas você também pode personalizar esses agentes conforme necessário.

2. **Ferramentas (Tools)**: São funções que um agente chama. É essencial fornecer ao agente as ferramentas corretas e descrevê-las de forma adequada para que o agente saiba como usá-las corretamente.

3. **Conjuntos de Ferramentas (Toolkits)**: Às vezes, o conjunto de ferramentas que um agente tem acesso é mais importante do que uma única ferramenta. A LangChain introduziu o conceito de toolkits, que são grupos de ferramentas necessárias para realizar objetivos específicos.

4. **Executor de Agente (AgentExecutor)**: É o runtime para um agente. Ele chama o agente e executa as ações que ele escolhe. Este executor lida com várias complexidades, como erros de ferramentas ou saídas de agentes que não podem ser analisadas.

### Uso de Agentes com a LangChain:

Para começar a construir um agente, você pode usar uma classe de agente da LangChain e personalizá-la para fornecer um contexto específico. Em seguida, defina ferramentas personalizadas e execute tudo no AgentExecutor padrão da LangChain.

Por exemplo, para criar um agente que calcule o comprimento de uma palavra, você pode definir uma ferramenta simples em Python e, em seguida, criar um prompt e um agente para usar essa ferramenta. Finalmente, você pode executar o agente usando o AgentExecutor.

Para mais detalhes e informações avançadas sobre agentes, consulte a [documentação oficial da LangChain](https://docs.langchain.com/docs/components/agents/).

## 🌐 Pesquisa na Wikipedia

A LangChain oferece uma ferramenta integrada para pesquisar e obter insights diretamente da Wikipedia, a maior e mais lida enciclopédia online do mundo. Esta ferramenta permite que os usuários acessem informações detalhadas e resumos de tópicos específicos da Wikipedia diretamente de sua aplicação.
