FROM python:3.10-slim

WORKDIR /app

COPY pyproject.toml .
RUN pip install --no-cache-dir .

COPY . .

EXPOSE 8080

CMD ["python3", "gcp-infrastructure/cloud_run/app.py"]
