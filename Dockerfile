FROM python:3.12-alpine3.19

# запрещает создавать файлы кеш (pyc)
ENV PYTHONDONTWRITEBYTECODE 1
# запрещает буфферизировать сообщения
ENV PYTHONUNBUFFERED 1

COPY ./webapi /backend
COPY requirements.txt /backend

WORKDIR /backend

RUN pip install -r requirements.txt
RUN pip install gunicorn

