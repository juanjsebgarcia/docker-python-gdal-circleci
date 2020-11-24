ARG BASE_IMAGE

FROM ${BASE_IMAGE}
LABEL maintainer="rumble.travel <juan@rumble.travel>"
LABEL version="3"

USER root

RUN apt-get update \
    && apt-get install sqlite3 \
    && rm -rf /var/lib/apt/lists/*

CMD python3 -V && pip -V
