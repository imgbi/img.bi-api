#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import web, json, string, random, M2Crypto, os, redis, bcrypt, hashlib, sha3, cgi
from zbase62 import zbase62
from datetime import datetime, timedelta
cgi.maxlen = 5 * 1024 * 1024
redis_server = 'localhost'
r_server = redis.Redis(redis_server)
upload_dir = '/home/img.bi/img.bi-files'
urls = (
  '/api/upload', 'upload',
  '/api/remove', 'remove',
)

class upload:
  def POST(self):
    web.header('Access-Control-Allow-Origin', '*')
    try:
      data = web.input()
    except ValueError:
      web.header("Content-Type", "application/json")
      return json.dumps({"status": "File is too large"})
    if not 'encrypted' in data:
      web.header("Content-Type", "application/json")
      return json.dumps({"status": "Wrong parameters"})
    try:
      json.loads(data.encrypted)
      if 'thumb' in data:
        json.loads(data.thumb)
    except ValueError:
      web.header("Content-Type", "application/json")
      return json.dumps({"status": "This is not JSON"})
    salt = r_server.get('salt')
    if salt is None:
      salt = zbase62.b2a(M2Crypto.m2.rand_bytes(25))
      r_server.set('salt', salt)
      r_server.expire('salt',86400)
    hashedip = hashlib.sha3_512(web.ctx.ip.encode('utf-8') + salt).hexdigest()
    redisip = r_server.get('ip:' + hashedip)
    if redisip is not None and int(redisip) > 100:
      web.header("Content-Type", "application/json")
      return json.dumps({"status": "Too much uploads from your IP"})
    fileid = ''.join(random.choice(string.letters + string.digits) for x in range(7))
    while r_server.get('file:' + fileid):
      fileid = ''.join(random.choice(string.letters + string.digits) for x in range(7))
    password = zbase62.b2a(M2Crypto.m2.rand_bytes(20))
    hashed = bcrypt.hashpw(password, bcrypt.gensalt())
    f = open(upload_dir + '/' + fileid,'w')
    f.write(data.encrypted)
    f.close()
    if 'thumb' in data:
      f = open(upload_dir + '/thumb/' + fileid,'w')
      f.write(data.thumb)
      f.close()
    if 'expire' in data and int(data.expire) != 0:
      try:
        delta = timedelta(days=int(data.expire))
      except:
        return json.dumps({"status": "Wrong expire date"})
      r_server.set('file:expire:' + fileid, (datetime.now() + delta).strftime('%Y-%m-%d %H:%M:%S'))
    r_server.set('file:' + fileid, hashed)
    r_server.incr('ip:' + hashedip)
    r_server.expire('ip:' + hashedip,86400)
    web.header("Content-Type", "application/json")
    return json.dumps({"id": fileid, "pass": password, "status": "OK"})

class remove:
  def GET(self):
    web.header('Access-Control-Allow-Origin', '*')
    data = web.input()
    if not all(x in data for x in ('id', 'password')):
      web.header("Content-Type", "application/json")
      return json.dumps({"status": "Wrong parameters"})
    if not r_server.get('file:' + data.id):
      web.header("Content-Type", "application/json")
      return json.dumps({"status": "No such file"})    
    hashed = r_server.get('file:' + data.id)
    if bcrypt.hashpw(data.password.encode('utf-8'), hashed) == hashed:
      os.remove(upload_dir + '/' + data.id)
      try:
        os.remove(upload_dir + '/thumb/' + data.id)
      except:
        pass
      r_server.delete('file:' + data.id)
      web.header("Content-Type", "application/json")
      return json.dumps({"status": "Success"})
    else:
      web.header("Content-Type", "application/json")
      return json.dumps({"status": "Wrong password"})

if __name__ == "__main__":
  web.wsgi.runwsgi = lambda func, addr=None: web.wsgi.runfcgi(func, addr)
  app = web.application(urls, globals())
  app.run()
