FROM alpine:3.9

RUN apk add --no-cache quassel-core qt5-qtbase-sqlite

EXPOSE 4242

CMD ["quasselcore", "--require-ssl", "-c", "/srv/quassel"]
