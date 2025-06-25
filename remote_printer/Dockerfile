FROM python:3.10-slim

RUN apt-get update && apt-get install -y cups libcups2-dev gcc && \
    pip install flask pycups && \
    apt-get clean

WORKDIR /app
COPY run.sh /run.sh
COPY app /app
RUN chmod +x /run.sh

CMD ["/run.sh"]