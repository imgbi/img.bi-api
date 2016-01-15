# DEPRECATED

This repo contains old version of img.bi backend. It's no longer required, new nodejs backend of img.bi available from [main repo](https://github.com/imgbi/img.bi).

# img.bi
[img.bi](https://img.bi/) is a secure image hosting. Images are encrypted using AES-256 with random key in browser before upload.

## About this repo
There is only Python script which process POST- and GET- requests. For work you need also [img.bi](https://github.com/imgbi/img.bi).  

## Configuration
Set ``upload_dir`` to directory where to upload files and ``redis_server`` for address of [Redis](http://redis.io) instance.

You need to change both ``code.py`` and ``expired.py`` files.

## How to run
``code.py`` runs by ``spawn-fcgi`` like this:

    spawn-fcgi -f code.py -a 127.0.0.1 -p 1234

After this you need to configure your webserver and serve this script on /api. Check [this](http://webpy.org/cookbook/fastcgi-nginx) for nginx example.

``expired.py`` is a script which remove expired images. You need to add a [cron](https://en.wikipedia.org/wiki/Cron) job for it.

## Dependencies
* [web.py](http://webpy.org/)
* [M2Crypto](http://chandlerproject.org/Projects/MeTooCrypto)
* [redis-py](https://github.com/andymccurdy/redis-py)
* [bcrypt](https://github.com/pyca/bcrypt/)
* [pysha3](https://pypi.python.org/pypi/pysha3)
* [zbase62](https://pypi.python.org/pypi/zbase62)

## Donate
Bitcoin: [1imgbioAKhqeSaAG2SB6Ct79r7UeyGpYP](bitcoin:1imgbioAKhqeSaAG2SB6Ct79r7UeyGpYP)

Litecoin: [LiMgBiGCWR3bYsHXLfZYonLBZpgCVqMAw2](litecoin:LiMgBiGCWR3bYsHXLfZYonLBZpgCVqMAw2)
