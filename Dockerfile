FROM python:3.12
RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y


EXPOSE 8080
WORKDIR /app

COPY . ./

RUN pip install -r requirements.txt

ENTRYPOINT ["streamlit", "run", "app.py", "--server.port=8080", "--server.address=0.0.0.0"]
