FROM python:3.10.19-slim-bookworm

WORKDIR /app

COPY requirements.txt .

RUN  apt-get update \
    && apt-get install -y \
    build-essential \
    cmake \
    libopenblas-dev \
    liblapack-dev \
    libx11-dev \
    ffmpeg \
    libsm6 \
    libxext6 \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip setuptools wheel
RUN pip install -r requirements.txt

CMD [ "python", "main.py" ]
