FROM python:3-slim
WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY . .
ENV DATA_DIR /data
EXPOSE 8080
ENTRYPOINT ["python3", "app.py"]