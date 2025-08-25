FROM python:3.6.8

WORKDIR /app

COPY . /app/

RUN pip install -r requirements.txt

CMD ["python", "app.py"]