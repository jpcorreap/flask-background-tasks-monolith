FROM python:3.8
COPY . / 
WORKDIR /backend
ENV PYTHONPATH=${PYTHONPATH}:${PWD} 
RUN apt-get update && apt-get install ffmpeg -y
RUN pip3 install poetry
RUN poetry config virtualenvs.create false
RUN poetry install --no-dev
