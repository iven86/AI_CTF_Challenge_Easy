FROM python:3.9-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Install system dependencies (required for torch and pillow)
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libjpeg-dev \
    zlib1g-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN pip install --no-cache-dir torch torchvision flask numpy pillow

# Copy challenge files
COPY model.pth /app/model.pth
COPY app.py /app/app.py
COPY base_image.png /app/base_image.png

# Set working directory
WORKDIR /app

# Expose port
EXPOSE 5000

# Run the Flask app
CMD ["python", "app.py"]
