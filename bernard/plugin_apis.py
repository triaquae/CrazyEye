#_*_coding:utf-8_*_


def sshtask(taskplan,stage_obj,job_obj,task_obj,*args,**kwargs):
    """run ssh commands"""
    #print("----calling sshtask plugin------")
    print(task_obj)

    exec_bindhosts = []
    exec_bindhosts.extend(task_obj.bind_hosts.all())
    for host_group in task_obj.host_groups.all():
        exec_bindhosts.extend(host_group.bind_hosts.all())
    print(set(exec_bindhosts))

    import threading
    from bernard.plugins import ssh_related
    from CrazyEye import settings

    #process_pool = threading.Pool(processes=settings.MaxTaskProcesses)

    res_list = []
    for bindhost in exec_bindhosts:

        p = threading.Thread(target=ssh_related.ssh_cmd_exec,args=(taskplan,task_obj,bindhost))
        #here needs to be changed to threading pool mode, for avoiding too many threads got started at the same time
        p.start()
        print("----start a thread for host %s---"% bindhost)
        res_list.append(p)
        taskplan.logger.info("---Started a thread for %s"%bindhost)

    for t in res_list:
        t.join()


def scptask(taskplan,stage_obj,job_obj,task_obj,*args,**kwargs):
    """run scp task"""


    exec_bindhosts = []
    exec_bindhosts.extend(task_obj.bind_hosts.all())
    for host_group in task_obj.host_groups.all():
        exec_bindhosts.extend(host_group.bind_hosts.all())
    print(set(exec_bindhosts))

    import threading
    from bernard.plugins import ssh_related
    from CrazyEye import settings


    res_list = []
    for bindhost in exec_bindhosts:
        p = threading.Thread(target=ssh_related.scp_task, args=(taskplan, task_obj, bindhost))
        # here needs to be changed to threading pool mode, for avoiding too many threads got started at the same time
        p.start()
        print("----start a thread for host %s---" % bindhost)
        res_list.append(p)
        taskplan.logger.info("---Started a thread for %s" % bindhost)

    for t in res_list:
        t.join()
