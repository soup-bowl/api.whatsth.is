FROM python:3-alpine

WORKDIR /usr/src/app

COPY requirements.txt ./

RUN apk add --no-cache yaml-dev

RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir gunicorn

COPY api api

EXPOSE 43594

ENTRYPOINT ["gunicorn", "-k", "uvicorn.workers.UvicornWorker", "-b", "0.0.0.0:43594", "api.main:app"]
