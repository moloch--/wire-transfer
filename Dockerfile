FROM python:3.10.12-slim-bullseye

RUN mkdir /wire-transfer /data

COPY . /wire-transfer

RUN chmod +x /wire-transfer/embed.py
RUN chmod +x /wire-transfer/english2bin.py
RUN chmod +x /wire-transfer/wiretransfer.py

WORKDIR /wire-transfer

RUN python3 -m pip install -r requirements.txt

# DEBUG
CMD /bin/bash
