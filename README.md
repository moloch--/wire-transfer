Wire Transfer
==============

Obfuscates downloads over HTTP by encoding binary files into English text and reconstructing the binary client side.

```
./wiretransfer.py --target=shell.exe
```


Setup
======

Install Python 2.7.x, then install the dependancies with:

```
pip install -r requirements.txt
```

Running from Docker :whale:
============================

Build:

```bash
docker build -f Dockerfile -t wire-transfer .
```

Run:

```bash
docker run -v $(pwd)/data:/data -it wire-transfer \
python embed.py --target=/data/meterp.exe \
--output=/data/meterp.html \
--attachment=meterp.exe
```