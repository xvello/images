FROM alpine:3.9

RUN apk add --no-cache fetchmail

CMD ["fetchmail", "--nodetach", "-f", "/local/fetch.conf"]
