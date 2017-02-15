from django.shortcuts import render,HttpResponse
from bernard import models
# Create your views here.

from  bernard import tasks

def task_test(request):

    res = tasks.add.delay(228,24)
    print("start running task")
    print("async task res",res.get() )

    return HttpResponse('res %s'%res.get())


def schedule_index(request):

    plans = models.Plan.objects.all()
    return render(request,"bernard/schedule_index.html",{'plans':plans})