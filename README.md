# c4p2n

_Created during the first B360R070N session._

**c4p2n** (Call For Paper To Notion) is a webhook to submit dasta about the talk
from TypeForm to our Notion.


## Usage

Use [Docker](https://docs.docker.com/) to run c4p2n.

First, build an image from the project root:

```shell
docker build -t %TAG_NAME% .
```

where `%TAG_NAME%` is something you'd like to tag your Docker image.

Now, you're go to go, run it:

```shell
docker run -it -d --name %CONTAINER_NAME% -p %PORT%:8000 %TAG_NAME%
```

where `%CONTAINER_NAME%` is something you'd like to name your Docker container,
`%PORT%` is a port you want to publish the app on, and `%TAG_NAME%` is the tag name
from the previous step.

This way you can run c4p2n as a separate app, proxy it with nginx or do
anything one can with a web application.

We run it in a FaaS fashion on [kintohub](https://kintohub.com) 

## Development

### Install dependencies

We use [Poetry](https://python-poetry.org/) for dependencies management.

To install dependencies from the project root run:

```shell
poetry install
```

### Run

For development purposes, you can skip the Docker part to not to bother with all
those fancy production accoutrements, and just use the run script:

```shell
sh run-app.sh [WORKERS_NUM] [PORT]
```

where `WORKERS_NUM` and `PORT` are optional and so far positional arguments,
so, beware.

If you want to reduce the overhead even more you can run the app with uvicorn:

```shell
uvicorn c4p2n.api:app
```

Now the app is up and running and you can find the OpenAPI schema at
http://localhost:8000/redoc for redoc and http://localhost:8000/docs for swagger.

### Lint and format

Currently we use [mypy](http://www.mypy-lang.org/) and
[black](https://github.com/psf/black).

### Contribute

_TODO link to CONTRBUTING.md_
