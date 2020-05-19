FROM tiangolo/uwsgi-nginx-flask:python3.7

RUN apt-get update && apt-get install -y unzip
WORKDIR /app
COPY ./src/requirements.txt .
RUN pip install -r requirements.txt
RUN PYTHONPATH=/app:$PYTHONPATH

COPY ./src /app


COPY custom_entrypoint.sh /custom_entrypoint.sh
RUN chmod +x /custom_entrypoint.sh

ENTRYPOINT ["/custom_entrypoint.sh"]

CMD ["/start.sh"]
