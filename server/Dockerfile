FROM python:3.12-slim

WORKDIR /app

COPY server/requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY server/ ./server
COPY proto/ ./proto

ENV PYTHONPATH=/app:/app/server:/app/proto

EXPOSE 9092
CMD ["python", "server/server.py"]
