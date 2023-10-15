#coding=utf-8
#!/usr/bin/env python3

bind = '127.0.0.1:9333'
workers = 3 #For 2 core
threads = 2 #Per worker optimum for 2 core and 512MB memory
max_requests = 1000 #Restart worker after 1000 requests
timeout = 30
max_requests_jitter = 100 #Restart connection after 100 req
errorlog = '/var/log/a2d_gu_error.log'
loglevel = 'error'
logrotate = 1000000 #rotate after 1MB
