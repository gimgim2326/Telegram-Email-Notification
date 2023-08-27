FROM python:3.9-slim-buster

ADD . /app
RUN cd /app && pip install -r requirements.txt

CMD ["python", "/app/server.py"]