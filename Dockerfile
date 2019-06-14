FROM python:3.6-alpine

RUN adduser -D netdiag

WORKDIR /home/netdiag

RUN python -m venv venv
COPY netDiag netDiag
RUN venv/bin/pip install -r ./netDiag/Server/requirements.txt

RUN chmod +x ./netDiag/Server/boot.sh

RUN chown -R netdiag:netdiag ./
USER netdiag

EXPOSE 8443
ENTRYPOINT ["./netDiag/Server/boot.sh"]
