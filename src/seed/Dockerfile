FROM ghcr.io/astral-sh/uv:python3.10-bookworm

RUN apt-get update && \
    apt-get install -y ttfautohint

VOLUME /work

WORKDIR /work

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
