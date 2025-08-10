# Use an official Python base image
FROM python:3.11-slim

# Create a non-root user and switch to it
RUN useradd -m nonroot
USER nonroot

# Set working directory
WORKDIR /app

# Copy all necessary files
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose Streamlit port
EXPOSE 8501

# Command to run your application
CMD ["streamlit", "run", "login.py"]

