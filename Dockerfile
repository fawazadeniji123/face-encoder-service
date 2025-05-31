FROM python:3.9-slim

# Install basic system dependencies needed for your app
RUN apt-get update && apt-get install -y --no-install-recommends \
    wget \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy your requirements.txt (without dlib, we install dlib manually)
COPY requirements.txt .

# Upgrade pip and setuptools
RUN pip install --upgrade pip setuptools wheel

# Install prebuilt dlib wheel for Python 3.9 on manylinux2014_x86_64
RUN pip install https://github.com/Davisking/dlib/releases/download/v19.24/dlib-19.24.0-cp39-cp39-manylinux2014_x86_64.whl

# Install other dependencies excluding dlib (make sure dlib NOT in requirements.txt)
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
