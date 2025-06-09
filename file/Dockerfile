FROM python:3.9-slim

WORKDIR /app

COPY file.py requirements.txt ./

RUN pip install -r requirements.txt

EXPOSE 5051

CMD ["python", "file.py"]

