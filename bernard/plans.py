#_*_coding:utf-8_*_

from bernard import models
from bernard import plugin_apis
import logging,json
from logging import handlers
from CrazyEye import settings


class TaskPlan(object):
    """analyze and run plan accordingly"""

    def __init__(self,plan_id):
        self.plan_id = plan_id
        self.plan_obj = models.Plan.objects.get(id=self.plan_id)
        self.set_logger()
        self.errors = []

    def set_logger(self):
        '''set logging format for this plan'''

        # create logger
        logger = logging.getLogger('PLAN:%s'% self.plan_obj)
        logger.setLevel(settings.LOG_LEVEL)

        # create console handler and set level to debug
        ch = logging.StreamHandler()
        ch.setLevel(settings.LOG_LEVEL)

        # create file handler and set level to warning
        fh = handlers.TimedRotatingFileHandler(filename="%s/plan_%s.log"%(settings.SCHEDULE_LOG_DIR,self.plan_id),
                                               when="D", interval=5, backupCount=30)

        #fh = logging.FileHandler("%s/plan_%s.log"%(settings.SCHEDULE_LOG_DIR,self.plan_id))
        fh.setLevel(settings.LOG_LEVEL)
        # create formatter
        formatter = logging.Formatter('%(asctime)s %(name)s %(levelname)s %(module)s:%(funcName)s:%(lineno)d %(message)s')

        # add formatter to ch and fh
        ch.setFormatter(formatter)
        fh.setFormatter(formatter)

        # add ch and fh to logger
        logger.addHandler(ch)
        logger.addHandler(fh)


        self.logger = logger
        # 'application' code

        # logger.critical('critical message')
    def plan_is_valid(self):
        """parse the plan before kickoff"""
        #plan_obj = models.Plan.objects.get(id=self.plan_id)
        #print("plan obj",plan_obj)
        #print(plan_obj.stage_set.all().order_by("order"))

        #self.plan_obj = plan_obj
        return True


    def run(self):
        """run plan tasks"""


        plan_log_obj = models.ScheduleLog.objects.create(plan=self.plan_obj,status=3)
        for stage in self.plan_obj.stage_set.all().order_by("order"):
            self.logger.info("start to run jobs in stage [%s]" % stage)
            for job in stage.job_set.all().order_by("order"):
                #print(job)
                task_model_obj = getattr(job,job.task_type)
                #call the related task plugin
                plugin_func = getattr(plugin_apis,job.task_type)
                print("---calling task %s---"% job.task_type)
                self.logger.info("running job [%s]"% job)
                plugin_func(self,stage,job,task_model_obj)
                print("---end of calling task %s---"% job.task_type)
                self.logger.info("job [%s] finished" % job)

        if self.errors:
            print("errors",self.errors)
            print("*"*150)
            plan_log_obj.errors = json.dumps(self.errors)
            plan_log_obj.status = 0
        else:
            plan_log_obj.status = 1

        plan_log_obj.save()
