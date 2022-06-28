# Dockerfile, Image, Container
FROM python:3.10.5

ADD GoogleDrive.py .
ADD Google.py .
ADD QuickStart.py .
ADD settings.yaml .
ADD client_secrets.json .

RUN pip install pydrive2
RUN pip install psycopg2
RUN pip install google-auth-oauthlib

RUN pip install requests


CMD [ "python", "./GoogleDrive.py" ]