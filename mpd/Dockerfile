FROM alpine:3.9

RUN apk add --no-cache mpd mpc ncmpc alsa-utils
ADD mpd.conf asound.conf /etc/

EXPOSE 6600

CMD ["mpd", "--no-daemon", "--stdout"]
