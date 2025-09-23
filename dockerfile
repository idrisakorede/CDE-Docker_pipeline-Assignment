# Use official Python 3.13 slim image
FROM python:3.13-slim

# Set the working directory inside the container
WORKDIR /app

# System dependencies for Playwright
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    libnss3 \
    libatk1.0-0 \
    libatk-bridge2.0-0 \
    libcups2 \
    libdrm2 \
    libxkbcommon0 \
    libxcomposite1 \
    libxdamage1 \
    libxrandr2 \
    libgbm1 \
    libasound2 \
    libxshmfence1 \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirement.txt .
RUN pip install --no-cache-dir -r requirement.txt

# Install Playwright browsers
RUN playwright install --with-deps chromium

# Copy scripts
COPY scraper.py .
COPY transform.py .
COPY load.py .

# Default command (to be overridden by run_pipeline.sh)
CMD ["python", "scraper.py"]
