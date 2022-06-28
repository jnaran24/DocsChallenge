# Dockerfile, Image, Container
FROM python:3.10.5

ADD GoogleDrive.py .

RUN pip install requests

CMD [ "python", "./main.py" ]