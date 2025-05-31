FROM python:3.9-slim

WORKDIR /app

# Install system dependencies needed for dlib and cmake
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    cmake \
    libopenblas-dev \
    liblapack-dev \
    libx11-dev \
    libgtk-3-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements.txt first
COPY requirements.txt .

# Install dlib first explicitly (you can specify the version if you want)
RUN pip install --no-cache-dir dlib

# Then install the rest of the requirements (without dlib in it)
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your application code
COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
