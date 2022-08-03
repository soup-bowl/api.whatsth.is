FROM python:3-slim

LABEL org.opencontainers.image.title="What's This API"
LABEL org.opencontainers.image.authors="code@soupbowl.io"
LABEL org.opencontainers.image.source="https://github.com/soup-bowl/api.whatsth.is"
LABEL org.opencontainers.image.licenses="MIT"

WORKDIR /usr/src/app

RUN pip install --no-cache-dir poetry

COPY pyproject.toml pyproject.toml
COPY poetry.lock    poetry.lock
COPY api            api

RUN poetry config virtualenvs.create false \
	&& poetry install --no-dev --no-interaction --no-ansi

EXPOSE 43594

ENTRYPOINT ["gunicorn", "-k", "uvicorn.workers.UvicornWorker", "-b", "0.0.0.0:43594", "api.main:app"]
