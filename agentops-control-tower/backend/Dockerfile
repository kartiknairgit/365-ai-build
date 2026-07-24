FROM python:3.12-slim
WORKDIR /app
COPY backend/pyproject.toml .
COPY backend/agentops agentops
COPY fixtures fixtures
RUN pip install --no-cache-dir .
EXPOSE 8000
CMD ["uvicorn", "agentops.main:app", "--host", "0.0.0.0", "--port", "8000"]
