FROM python:3.10.19-slim-trixie

WORKDIR /app

COPY . .

RUN  apt-get update \
    && apt-get install -y wget build-essential pkg-config libprotobuf-dev protobuf-compiler cmake libopenblas-dev liblapack-dev \
    && rm -rf /var/lib/apt/lists/*

RUN wget https://files.pythonhosted.org/packages/41/9f/838762bcfd3236d66e196b8c076c8bd26d749b9c52947a6b9201be034668/mediapipe-0.10.21-cp310-cp310-manylinux_2_28_x86_64.whl

RUN pip install -r requirements.txt

CMD [ "compare.py" ]
