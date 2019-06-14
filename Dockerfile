FROM python:3.7-alpine

RUN adduser -D netdiag

WORKDIR /home/netdiag

RUN apk update && apk upgrade && \
    apk add --no-cache git 

RUN python -m venv venv
RUN git clone https://github.com/cbabs/netDiag.git
RUN venv/bin/pip install -r ./netDiag/Server/requirements.txt

RUN chmod +x ./netDiag/Server/boot.sh

RUN chown -R netdiag:netdiag ./
USER netdiag

EXPOSE 8443
ENTRYPOINT ["./netDiag/Server/boot.sh"]
