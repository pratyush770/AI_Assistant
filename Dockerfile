# Use an official Python base image
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

RUN apt-get update && apt-get install -y build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy all necessary files
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir pytest pytest-cov

COPY . .

# Expose Streamlit port
EXPOSE 8501

# Command to run your application
CMD ["streamlit", "run", "login.py", "--server.address=0.0.0.0", "--server.port=8501"]


