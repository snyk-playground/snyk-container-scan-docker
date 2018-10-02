FROM python:3.6.4-alpine3.7

ENV LANG C.UTF-8

COPY packages/snyk-linux /usr/local/bin/snyk-linux

RUN apk update && \
    apk upgrade && \
    apk add --no-cache \
        docker \
        git \
        nodejs && \
    pip install requests && \
    npm install codefresh -g && \
    npm install snyk -g && \
    chmod +x /usr/local/bin/snyk-linux

COPY scripts/snyk-cli.py /snyk-cli.py

CMD [""]
