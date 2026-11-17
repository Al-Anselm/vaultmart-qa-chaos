FROM python:3.12-slim

WORKDIR /app

RUN pip install --no-cache-dir flask

COPY app/server.py /app/server.py

EXPOSE 8000

CMD ["python", "server.py"]
