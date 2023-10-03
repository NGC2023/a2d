#coding=utf-8
#!/usr/bin/env python3

bind = '127.0.0.1:9333'
workers = 8 #For 4 core, each 2 workers
threads = 2 #Per worker optimum for 4 core and 1GB memory
max_requests = 1000 #Restart worker after 1000 requests
timeout = 30
max_requests_jitter = 100 #Restart connection after 100 req
errorlog = '/var/log/a2d_gu_error.log'
loglevel = 'error'
logrotate = 1000000 #rotate after 1MB
