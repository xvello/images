FROM ubuntu:xenial as builder

RUN apt-get update \
 && apt-get install -y \
    build-essential git \
    libx11-dev libimlib2-dev

RUN git clone https://github.com/Tomas-M/xlunch.git \
 && cd xlunch \
 && make xlunch


FROM ubuntu:xenial

RUN apt-get update \
 && apt-get install -y --no-install-recommends software-properties-common \
 && add-apt-repository ppa:team-xbmc/ppa \
 && apt-get update \
 && apt-get install -y --no-install-recommends \
    xserver-xorg-input-libinput xserver-xorg-video-intel xserver-xorg-core xinit \
    kodi kodi-inputstream-rtmp kodi-inputstream-adaptive \
    kodi-peripheral-joystick \
    libimlib2 fonts-roboto rofi \
 && rm -rf /var/lib/apt/lists/*

RUN echo "/xlunch --config /xlunch.config" > /root/.xinitrc
COPY --from=builder /xlunch/xlunch /xlunch

CMD ["startx"]
