FROM nginx:alpine

RUN apk add --no-cache git \
 && rm -rf /usr/share/nginx/html \
 && git clone https://github.com/xvello/html-password-generator.git /usr/share/nginx/html
