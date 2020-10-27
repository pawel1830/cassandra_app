FROM python:3.8 as builder

ARG environment=dev

RUN pip install pipenv
COPY $environment.requirements.in ./

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN pip-compile $environment.requirements.in > requirements.txt
RUN pip install --user -r requirements.txt

FROM python:3.8-alpine

WORKDIR /app


ENV LANG pl_PL.UTF-8
ENV LANGUAGE pl_PL.UTF-8
ENV LC_ALL pl_PL.UTF-8
ENV CASSANDRA_HOSTS localhost


EXPOSE 8080

RUN ls -l

COPY --from=builder /root/.local /root/.local
ENV PATH=/root/.local/bin:$PATH


COPY test_project /app/test_project/
COPY manage.py /app/
COPY check_cassandra.py /app/
COPY entrypoint.sh /entrypoint.sh


ENTRYPOINT ["/entrypoint.sh"]
CMD ["uwsgi","test_project/uwsgi_api.ini"]