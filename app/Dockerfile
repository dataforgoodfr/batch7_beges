FROM tiangolo/uwsgi-nginx-flask:python3.7

RUN apt-get update && apt-get install -y unzip
WORKDIR /app
COPY ./src/requirements.txt .
RUN pip install -r requirements.txt
RUN PYTHONPATH=/app:$PYTHONPATH

COPY ./src /app
