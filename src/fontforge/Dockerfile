FROM alpine:latest

RUN apk add --no-cache \
    font-noto \
    fontforge-gui

RUN adduser -D -H user

USER user

ENTRYPOINT ["/usr/bin/fontforge-gui"]
