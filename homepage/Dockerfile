FROM nginx:alpine

RUN apk add --no-cache git \
 && rm -rf /usr/share/nginx/html \
 && git clone https://github.com/xvello/homepage-navigation.git /usr/share/nginx/html
