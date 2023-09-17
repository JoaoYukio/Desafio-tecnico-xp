FROM python:3.11

ENV HOST=0.0.0.0
ENV LISTEN_PORT 8080

EXPOSE 8080

RUN apt-get update && apt-get install -y git

WORKDIR /app

RUN pip install pipenv

COPY Pipfile Pipfile.lock ./

RUN pipenv install --deploy --ignore-pipfile

ENV PATH="/root/.local/bin:$PATH"

COPY ./src /app/src
COPY ./src/.streamlit /app/.streamlit

CMD ["pipenv", "run", "streamlit", "run", "src/main.py", "--server.port", "8080"]

