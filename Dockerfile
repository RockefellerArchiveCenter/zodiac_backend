FROM python:3.11

ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
ADD requirements.txt /code/
RUN python -m pip install --upgrade "pip>=26.2.2" && \
    python -m pip install -r requirements.txt
ADD . /code/
