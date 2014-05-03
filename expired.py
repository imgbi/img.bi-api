#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import redis, os
from datetime import datetime
redis_server = 'localhost'
r_server = redis.Redis(redis_server)
upload_dir = '/home/img.bi/img.bi-files'

for value in r_server.keys('file:expire:*'):
  if datetime.strptime(r_server.get(value),'%Y-%m-%d %H:%M:%S') < datetime.now():
    fileid = value.replace('file:expire:','')
    os.remove(upload_dir + '/' + fileid)
    try:
      os.remove(upload_dir + '/thumb/' + fileid)
    except:
      pass
    r_server.delete('file:' + fileid)
    r_server.delete(value)
