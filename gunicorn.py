# gunicorn.py
import logging
import logging.handlers
from logging.handlers import WatchedFileHandler
import os
import multiprocessing

bind = '127.0.0.1:8002'      		# 绑定ip和端口号
pidfile = "/xxx/xxx/xxx/gunicorn_log/gunicorn.pid"
backlog = 512               		# 监听队列
#chdir = '/home/test/server/bin'  	# gunicorn要切换到的目的工作目录
timeout = 30                 		# 超时

workers = multiprocessing.cpu_count() * 2 + 1    # 进程数
worker_class = 'gevent'      # 使用gevent模式，还可以使用sync 模式，默认的是sync模式

threads = 2 				 # 指定每个进程开启的线程数
loglevel = 'error' 			 # 日志级别，这个日志级别指的是错误日志的级别，而访问日志的级别无法设置
access_log_format = '%(t)s %(p)s %(h)s "%(r)s" %(s)s %(L)s %(b)s %(f)s" "%(a)s"'    # 设置gunicorn访问日志格式，错误日志无法设置

reload = True				# 设置reload 为True 只要项目代码有所修改，会自动重启

"""
其每个选项的含义如下：
h          remote address
l          '-'
u          currently '-', may be user name in future releases
t          date of the request
r          status line (e.g. ``GET / HTTP/1.1``)
s          status
b          response length or '-'
f          referer
a          user agent
T          request time in seconds
D          request time in microseconds
L          request time in decimal seconds
p          process ID
"""
accesslog = "/xxx/xx/xxx/gunicorn_log/gunicorn_access.log"      #访问日志文件
errorlog = "/xxx/xxx/xxx/gunicorn_log/gunicorn_error.log"        #错误日志文件


"""  其他参考配置

import os
import gevent.monkey
gevent.monkey.patch_all()

import multiprocessing

# debug = True
loglevel = 'debug'
bind = "0.0.0.0:7001"
pidfile = "log/gunicorn.pid"
accesslog = "log/access.log"
errorlog = "log/debug.log"
daemon = True

# 启动的进程数
workers = multiprocessing.cpu_count()
worker_class = 'gevent'
x_forwarded_for_header = 'X-FORWARDED-FOR'

"""
