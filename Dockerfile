FROM python:3.8

WORKDIR /opt/project

COPY pyproject.toml poetry.lock /opt/project/

# Turn off auto creation of venvs, use system-wide python in docker image
RUN pip install poetry>=1.0.0 && \
    poetry config virtualenvs.create false && \
    poetry install && \
    pip install gunicorn==20

COPY . /opt/project/

CMD ["gunicorn", "c4p2n.api:app", "--workers=1", "--worker-class=uvicorn.workers.UvicornWorker", "--bind=0.0.0.0:8000"]
