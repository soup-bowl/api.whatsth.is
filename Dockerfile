FROM python:3-alpine

WORKDIR /usr/src/app

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY api api

EXPOSE 43594

ENTRYPOINT [ "python", "-m", "api" ]
