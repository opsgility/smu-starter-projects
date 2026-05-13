FROM mcr.microsoft.com/azurelinux/base/python:3.12 AS build
WORKDIR /app
COPY worker/requirements.txt .
RUN python3 -m venv /opt/venv \
 && /opt/venv/bin/pip install --no-cache-dir --upgrade pip \
 && /opt/venv/bin/pip install --no-cache-dir -r requirements.txt

FROM mcr.microsoft.com/azurelinux/base/python:3.12
ENV PATH=/opt/venv/bin:$PATH \
    PYTHONUNBUFFERED=1
WORKDIR /app
COPY --from=build /opt/venv /opt/venv
COPY worker/ ./worker/
CMD ["python", "-m", "worker.worker"]
