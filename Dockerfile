FROM python:3.12
RUN apt-get update && apt-get install -y \
    libopencv-dev \
    libgl1-mesa-dev \
    && rm -rf /var/lib/apt/lists/*

EXPOSE 8080
WORKDIR /app

COPY . ./

RUN pip install -r requirements.txt

ENTRYPOINT ["streamlit", "run", "app.py", "--server.port=8080", "--server.address=0.0.0.0"]
