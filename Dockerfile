FROM python:3.10-slim

# System deps
RUN apt-get update && apt-get install -y \
    git \
    libglib2.0-0 \
    libsm6 \
    libxrender1 \
    libxext6 \
    ffmpeg \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install Python deps
COPY requirements.txt /app/requirements.txt
WORKDIR /app
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy API
COPY app.py /app/app.py

EXPOSE 8000
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
