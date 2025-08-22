FROM python:3.6.8

WORKDIR /app

COPY ./app.py ./requirements.txt ./tests /app/

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "app.py"]