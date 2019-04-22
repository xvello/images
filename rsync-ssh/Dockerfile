FROM alpine:3.9

RUN apk add --no-cache s6 openssh-client rsync tzdata autossh
ADD services /services/
RUN mkdir /backups/

CMD ["s6-svscan", "/services/"]
