#_*_coding:utf-8_*_

from celery import Celery

import time,os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "CrazyEye.settings")

app = Celery('tasks',
             broker='redis://localhost',
             backend='redis://localhost')



@app.task
def add(x,y):
    print("running...",x,y)
    #time.sleep(5)
    return x+y


@app.task
def call_back():
    print('----other...')
    return True


