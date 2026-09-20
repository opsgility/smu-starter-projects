# Small production image for the Ridgevault portfolio-review flow.
# The lab container variant (python-ai) already has these packages preinstalled for local dev;
# this Dockerfile is what Container Apps runs in Azure, so it installs them fresh into a slim base.
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src/ ./src/

EXPOSE 8080

# uvicorn honors the PORT env var Container Apps injects (defaults to 8080).
CMD ["uvicorn", "src.portfolio_flow:app", "--host", "0.0.0.0", "--port", "8080"]
