FROM docker.io/library/ubuntu:22.04

RUN ln -sf /usr/share/zoneinfo/Asia/Tokyo /etc/localtime

RUN apt-get update && \
    apt-get install -y \
    fontforge \
    parallel \
    ttfautohint \
    python-is-python3 \
    python3 \
    python3-fontforge \
    python3-pip

COPY requirements.txt .

RUN pip install -r requirements.txt

VOLUME /work

WORKDIR /work

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
