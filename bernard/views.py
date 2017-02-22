from django.shortcuts import render,HttpResponse
from bernard import models
import json
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



def plan_detail(request,plan_id):
    plan_obj = models.Plan.objects.get(id=plan_id)
    return render(request,"bernard/plan_detail.html", locals())



def save_task_order(request,plan_id):
    print(request.POST)

    task_orders = json.loads(request.POST.get('tasks'))
    #format: [['1', ['3', '1']], ['2', ['2', '4', '5']]]

    print(task_orders)
    for index,i in enumerate(task_orders):
        print(index,i)
        stage_obj = models.Stage.objects.get(id=i[0])
        stage_obj.order = index
        stage_obj.save()
        job_ids = i[1]
        for job_index,job_id in enumerate(job_ids):
            job_obj = models.Job.objects.get(id=job_id)
            job_obj.order = job_index
            job_obj.save()

    return HttpResponse(json.dumps({'state':'success'}))
