FROM python:3.9.9-alpine3.14 AS builder
WORKDIR /api
ADD requirements.txt /api
RUN apk add gcc g++ musl-dev
RUN pip install -r requirements.txt

FROM python:3.9.9-alpine3.14
WORKDIR /api
ADD . /api
COPY --from=builder /usr/local/lib/python3.9/site-packages /usr/local/lib/python3.9/site-packages