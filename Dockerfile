FROM python:3-alpine

WORKDIR /usr/src/app

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY api            api
COPY detection.json detection.json

EXPOSE 43594
CMD [ "python", "-m", "api" ]
