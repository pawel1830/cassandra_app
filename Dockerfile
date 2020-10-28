FROM python:3.8-alpine AS builder
RUN apk --update add build-base linux-headers musl musl-dev musl-utils bash python3 python3-dev py-pip


RUN pip install pip-tools
COPY requirements.in ./

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN pip install --upgrade pip
RUN pip-compile requirements.in > requirements.txt
RUN pip install --user -r requirements.txt

FROM python:3.8-alpine

WORKDIR /app


ENV LANG pl_PL.UTF-8
ENV LANGUAGE pl_PL.UTF-8
ENV LC_ALL pl_PL.UTF-8
ENV CASSANDRA_HOSTS localhost
ENV DEBUG 0


EXPOSE 8080

RUN ls -l

COPY --from=builder /root/.local /root/.local
COPY --from=builder /usr/local/lib/python3.8/site-packages /usr/local/lib/python3.8/site-packages/

ENV PATH=/root/.local/bin:$PATH


COPY test_project /app/test_project/
COPY manage.py /app/
COPY check_cassandra.py /app/
COPY entrypoint.sh /entrypoint.sh


ENTRYPOINT ["/entrypoint.sh"]
CMD ["uwsgi","test_project/uwsgi_api.ini"]