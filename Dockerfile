# syntax=docker/dockerfile:1
FROM python:3.14-alpine

ARG APP_NAME="app"
ENV WORKDIR=/opt/python/${APP_NAME}
ENV VIRTUAL_ENV=/opt/python/venv
ENV BUILD_ENV=/opt/python

RUN set -eux; \
   addgroup -g 935 -S python; \
   adduser -u 935 -S -D -G python -H -h /opt/python -s /bin/ash python; \
   install --verbose --directory --owner python --group python --mode 1755 /opt/python
   
RUN apk add --no-cache \
   openssl \
   fuse3 \
   postgresql18-client \
   inotify-tools \
   git

USER python

RUN python -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
ENV PYTHONPATH=$WORKDIR

COPY requirements.txt .

RUN pip install --upgrade pip \
    && pip install -r requirements.txt

COPY .gitignore "${BUILD_ENV}"
COPY pyproject.toml "${BUILD_ENV}"
COPY README.md "${BUILD_ENV}"

CMD [ "python" ]