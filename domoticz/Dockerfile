FROM debian:stable-slim

ARG DEBIAN_FRONTEND=noninteractive
ENV PATH="$PATH:/opt/domoticz/" \
    DEB_DEPS_BASE="dumb-init curl libcurl3-gnutls libusb-0.1-4 libssl1.0.0/jessie" \
    DEB_DEPS_PY35="libpython3.5 python3-pip python3-wheel python3-setuptools" \
    DEB_DEPS_CUST="netcat" \
    PIP_DEPS="broadlink pyaes" \
    TGZ_URL="https://releases.domoticz.com/releases/release/domoticz_linux_x86_64.tgz"
    #TGZ_URL="https://releases.domoticz.com/releases/beta/domoticz_linux_x86_64.tgz"

# Official binaries require an old libssl
RUN echo "deb http://deb.debian.org/debian jessie main" > \
    /etc/apt/sources.list.d/jessie.list

# To enable domoticz to find libpython3.5.so
RUN echo "/usr/lib/python3.5/config-3.5m-x86_64-linux-gnu" > /etc/ld.so.conf.d/python.conf

RUN apt-get update \
 && apt-get install --no-install-recommends -y $DEB_DEPS_BASE $DEB_DEPS_PY35 $DEB_DEPS_CUST \
 && python3 -m pip install $PIP_DEPS \
 && rm -rf /var/lib/apt/lists/* /root/.cache

WORKDIR /opt/domoticz/
RUN curl -sL $TGZ_URL | tar xzf -

# Make sure all deps are linking OK
RUN domoticz -version

VOLUME /config
CMD ["dumb-init", "domoticz", "-userdata", "/config"]