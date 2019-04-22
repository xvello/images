FROM alpine:3.9

RUN apk add --no-cache dnsmasq tini

EXPOSE 53 53/udp

ENTRYPOINT ["/sbin/tini", "--"]
CMD ["dnsmasq", "-k", "-S", "/consul/127.0.0.1#8600"]