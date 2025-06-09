FROM python:3.9-slim

WORKDIR /app

COPY user.py requirements.txt ./

RUN pip install -r requirements.txt

EXPOSE 5050

CMD ["python", "user.py"]

