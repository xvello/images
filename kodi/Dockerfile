FROM ubuntu:bionic

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

COPY start.sh /usr/local/bin/

CMD ["startx", "/usr/local/bin/start.sh"]
