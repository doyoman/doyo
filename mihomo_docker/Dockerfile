FROM alpine:latest

RUN mkdir /app

COPY bin/* /usr/bin/
COPY data /opt/data

EXPOSE 9090 7890

CMD [ "/usr/bin/start.sh" ]