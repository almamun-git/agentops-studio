FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY pyproject.toml /app/pyproject.toml
RUN pip install -U pip && pip install --no-cache-dir -e .

# Copy application code
COPY app /app/app

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]


