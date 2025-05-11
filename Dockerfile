FROM python:3.11-slim

# Install Tkinter dependencies
RUN apt-get update && \
    apt-get install -y python3-tk && \
    rm -rf /var/lib/apt/lists/*

# Set working dir and copy app
WORKDIR /app
COPY . .

# Default command
CMD ["python3", "main.py"]
