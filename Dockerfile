FROM python:3.8-alpine
COPY *.txt /



WORKDIR /app

RUN apk update && \
    apk add --virtual build-deps gcc python3-dev musl-dev linux-headers libffi-dev make

# Install python libraries
RUN pip install --upgrade pip && \
    pip install -r /requirements.txt

RUN apk del build-deps

COPY . /app/
COPY entrypoint.sh /entrypoint.sh
COPY delete_unnecessary_messages.sh /etc/periodic/15min/


EXPOSE 8080
ENV LANG pl_PL.UTF-8
ENV LANGUAGE pl_PL.UTF-8
ENV LC_ALL pl_PL.UTF-8
ENV CASSANDRA_HOST localhost

ENTRYPOINT ["/entrypoint.sh"]
CMD ["uwsgi","test_project/uwsgi_api.ini"]