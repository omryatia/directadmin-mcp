FROM python:3.12-slim

WORKDIR /app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=8888

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create directories
RUN mkdir -p logs

# Set permissions
RUN chmod +x server.py client.py

# Expose port
EXPOSE ${PORT}

# Set default command
CMD ["python", "main.py"]