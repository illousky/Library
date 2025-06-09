FROM python:3.9-slim 

WORKDIR /app

COPY client.py requirements.txt /data ./

RUN pip install -r requirements.txt

CMD ["python", "client.py"]
