FROM jehernandezr/python_38_ffmpeg:latest
COPY . /application 
WORKDIR /application/backend
VOLUME /application/
ENV PYTHONPATH=${PYTHONPATH}:${PWD} 
RUN pip3 install poetry
RUN poetry config virtualenvs.create false
RUN poetry install --no-dev
