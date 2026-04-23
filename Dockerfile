FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install
COPY requirements_api.txt .
RUN pip install --no-cache-dir -r requirements_api.txt

# Copy the rest of the application
COPY . .

# Expose the API port
EXPOSE 8080

# Run the API
CMD ["python", "bob_api.py"]
