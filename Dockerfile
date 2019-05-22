FROM debian

RUN apt-get update && apt-get install -y \
    rabbitmq-server \
    python3-dev \
    python3-pip

ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
COPY . /code/
ADD requirements /code/requirements
RUN pip3 install -r requirements/requirements.txt

