FROM python:3.8
MAINTAINER meetup@piterpy.ru

ENV PORT=8000
ENV HOST=0.0.0.0

WORKDIR /opt/project

ADD pyproject.toml poetry.lock /opt/project/

# Turn off auto creation of venvs, use system-wide python in docker image
RUN pip install poetry>=1.0.0 && \
    poetry config virtualenvs.create false && \
    poetry install

ADD . /opt/project/

CMD uvicorn --host=$HOST --port=$PORT c4p2n.api:app