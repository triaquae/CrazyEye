# Create your tasks here
from __future__ import absolute_import, unicode_literals
from celery import shared_task
from bernard.plans import  TaskPlan

@shared_task
def add(x, y):
    print("runninig add", x,y)
    return "add res:",x + y


@shared_task
def mul(x, y):
    return x * y


@shared_task
def xsum(numbers):
    return sum(numbers)

@shared_task
def scp_task(file):
    print("running scp file",file)
    return  "done"


@shared_task
def task_plan(plan_id):
    print("plan id ", plan_id)

    plan_runner_obj = TaskPlan(plan_id)
    if plan_runner_obj.plan_is_valid():
        plan_runner_obj.run()