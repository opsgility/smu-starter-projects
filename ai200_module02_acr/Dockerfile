# Multi-stage build for the Northwind shipment-classifier.
# Base image is Azure Linux 3.0 Python 3.12 (Microsoft-supported).
FROM mcr.microsoft.com/azurelinux/base/python:3.12 AS build

WORKDIR /app
COPY requirements.txt .
RUN python -m venv /opt/venv \
 && /opt/venv/bin/pip install --no-cache-dir --upgrade pip \
 && /opt/venv/bin/pip install --no-cache-dir -r requirements.txt

FROM mcr.microsoft.com/azurelinux/base/python:3.12

ENV PATH=/opt/venv/bin:$PATH \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=8000

WORKDIR /app
COPY --from=build /opt/venv /opt/venv
COPY app/ ./app/

EXPOSE 8000
HEALTHCHECK --interval=30s --timeout=5s CMD curl -fsS http://127.0.0.1:8000/healthz || exit 1

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
