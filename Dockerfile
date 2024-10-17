FROM python:3.12-alpine

COPY . /forum-baca
WORKDIR /forum-baca
RUN pip install -r requirements.txt

CMD [ "python","manage.py","runserver" ,"0.0.0.0:8000"]
