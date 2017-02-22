#_*_coding:utf-8_*_

import datetime
import re,os,time,json
from django import template

from django.utils.safestring import mark_safe,mark_for_escaping
from  django.core.urlresolvers import reverse as url_reverse
from CrazyEye import settings
from bernard import models
register = template.Library()


@register.simple_tag
def get_plan_last_runlog(plan_obj):
    # plan_log =  "%s/plan_%s.log" % (settings.SCHEDULE_LOG_DIR,plan_obj.id)
    #
    # if os.path.isfile(plan_log):
    #     last_run_time = time.strftime("%Y-%m-%d %H:%M:%S",
    #                                   time.gmtime(os.stat(plan_log).st_mtime) )
    # else:
    #     last_run_time = "Never Run"
    #
    # return last_run_time
    return plan_obj.schedulelog_set.last()


@register.simple_tag
def get_plan_crontab(plan_obj):

    #lowlowlow
    try:
        task_obj = models.PeriodicTask.objects.get(args=json.dumps([plan_obj.id]))

        return task_obj
    except Exception as e:
        return None


@register.simple_tag
def  get_plan_stages_in_order(plan_obj):
    return  plan_obj.stage_set.order_by('order')


@register.simple_tag
def get_stages_jobs_in_order(stage):
    return stage.job_set.order_by('order')