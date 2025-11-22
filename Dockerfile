FROM python:3.11-slim

# Prevent Python from writing .pyc files & enable unbuffered output
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Copy only requirements first for caching
COPY FastApi_app/requirements.txt /app/requirements.txt

# Install dependencies without build tools
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY FastApi_app/ /app/

# Expose port
EXPOSE 8000

# Start App
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
