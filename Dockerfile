FROM python:3.12-alpine3.19

# запрещает создавать файлы кеш (pyc)
ENV PYTHONDONTWRITEBYTECODE 1
# запрещает буфферизировать сообщения
ENV PYTHONUNBUFFERED 1

RUN apk update && apk upgrade && apk add bash
RUN python -m pip install --upgrade pip
RUN mkdir /backend

COPY ./webapi /backend
COPY requirements.txt /backend

WORKDIR /backend

RUN pip install -r requirements.txt
RUN pip install gunicorn

RUN mkdir -p /var/www/webapi/static && mkdir /var/www/webapi/media

ENTRYPOINT ["/bin/sh", "-c" , "./django_db_wait.sh && ./django_init.sh"]

#EXPOSE 8000
#CMD ["python","manage.py","runserver","0.0.0.0:8000"]