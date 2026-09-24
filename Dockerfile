FROM python:3.13.14-alpine

RUN apk add --no-cache gcc musl-dev linux-headers

COPY ./requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY ./app ./app

ENTRYPOINT ["sh", "-c"]