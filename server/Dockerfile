FROM python:3.12-slim
WORKDIR /app

COPY server/requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY proto/  ./proto
COPY server/ ./server
COPY server/.env /app/.env

RUN python -m grpc_tools.protoc \
    -I proto \
    --python_out=proto/generated \
    --grpc_python_out=proto/generated \
    proto/user.proto proto/weather.proto

RUN rm -rf proto/google

ENV PYTHONPATH=/app:/app/server:/app/proto:/app/proto/generated

EXPOSE 9092
CMD ["python", "server/server.py"]
