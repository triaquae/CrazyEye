#_*_coding:utf-8_*_
import paramiko
import traceback
import web,bernard
from CrazyEye import settings
import os

def ssh_cmd_exec(taskplan,task_obj,bind_host ):
    # task_obj = bernard.models.Task.objects.get(id=task_id)
    # bind_host = web.models.BindHosts.objects.get(id=bind_host_id)
    print("ssh cmd exec:",task_obj.commands,bind_host)
    s = paramiko.SSHClient()
    s.load_system_host_keys()
    s.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    taskplan.logger.info("connecting remote host %s:%s:%s"% (bind_host.host.ip_addr,bind_host.host.port,bind_host.host_user.username))
    try:
        if bind_host.host_user.auth_method == 'ssh-password':
            s.connect(bind_host.host.ip_addr,
                      int(bind_host.host.port),
                      bind_host.host_user.username,
                      bind_host.host_user.password,
                      timeout=5)
        else:#rsa_key

            key = paramiko.RSAKey.from_private_key_file(settings.RSA_PRIVATE_KEY_FILE)
            s.connect(bind_host.host.ip_addr,
                      int(bind_host.host.port),
                      bind_host.host_user.username,
                      pkey=key,
                      timeout=5)

        taskplan.logger.debug("logon [%s] success,executing commands \n%s" % (bind_host,task_obj.commands))
        stdin,stdout,stderr = s.exec_command(task_obj.commands)
        result = stdout.read(),stderr.read()
        if any(result):
            #cmd_result = filter(lambda x:len(x.strip())>0,result)[0]
            cmd_result = result[0] if result[0] else result[1]
        else:
            cmd_result = b'execution has no output!'
        res_status = 'success'
        print('----------- HOST:%s  IP:%s -------------' %(bind_host.host.hostname,bind_host.host.ip_addr) )

        # for line in cmd_result.decode():
        #     print(line)
        print(cmd_result.decode())
        s.close()
        taskplan.logger.info("%s cmd exec result \n%s" % (bind_host, cmd_result))
    except Exception as e:
        print('----------- HOST:%s  IP:%s -------------' %(bind_host.host.hostname,bind_host.host.ip_addr))
        print('\033[31;1mError:%s\033[0m' % e)
        print(traceback.print_exc())
        cmd_result = e
        res_status = 'failed'
        taskplan.logger.info("%s  %s " % (bind_host, cmd_result))
        taskplan.errors.append({'ssh_cmd_exec':"host %s , error %s" %(bind_host,e)})

def scp_task(taskplan,task_obj,bind_host ):
    """
    run scp
    :param taskplan: Plan Instance
    :param task_obj: bernard.models.Task
    :param bind_host: web.models.BindHosts
    :return:
    """


    try:
        t = paramiko.Transport((bind_host.host.ip_addr, int(bind_host.host.port)))
        taskplan.logger.info("connecting host %s "%bind_host)
        if bind_host.host_user.auth_method == 'ssh-password':

            t.connect(username=bind_host.host_user.username, password=bind_host.host_user.password)
        else:
            key = paramiko.RSAKey.from_private_key_file(settings.RSA_PRIVATE_KEY_FILE)
            t.connect(username=bind_host.host_user.username, pkey=key)

        sftp = paramiko.SFTPClient.from_transport(t)

        cmd_result = ''
        #if task_type == 'file_send':
            # local_file_list =content[content.index('-local') +1].split()
        local_file_path = "%s/task_data/files/%s" % (settings.FileUploadDir,task_obj.local_path)
        if os.path.isdir(local_file_path):
            for filename in os.listdir(local_file_path):
                local_file = "%s/%s" % (local_file_path, filename)

                remote_file_path = '%s/%s' % (task_obj.remote_path, filename)
                # print(local_file,remote_file_path)

                sftp.put(local_file, remote_file_path)
                # cmd_result += '%s  ' %filename
                cmd_result += "file [%s] sent to remote path [%s] is completed\n" % (filename, task_obj.remote_path)
                # print("----->cmd result:",cmd_result)

        else:
            local_filename = local_file_path.split("/")[-1]
            remote_path = os.path.join(task_obj.remote_path,local_filename)
            sftp.put(local_file_path,remote_path)
            cmd_result += "file [%s] sent to remote path [%s] is completed\n" % (local_filename, task_obj.remote_path)

        taskplan.logger.info("file sent to [%s] result:\n%s" %(bind_host,cmd_result))
        # else:
        #
        #     local_path = "%s/task_data/%s/" % (settings.FileUploadDir, task_id)
        #
        #     remote_filename = remote_path.split("/")[-1]
        #     local_file_path = "%s.%s" % (remote_filename, bind_host.host.ip_addr)
        #     print('->file get:', local_file_path, remote_filename)
        #     sftp.get(remote_path, '%s/%s' % (local_path, local_file_path))
        #     cmd_result = 'download remote file [%s] is completed!' % remote_path

        res_status = 'success'
    except Exception as e:
        print(e)
        cmd_result = e
        res_status = 'failed'

        taskplan.logger.error("file sent to [%s] result:\n%s" % (bind_host, cmd_result))
        taskplan.errors.append({'scp_task':"host %s , error %s" %(bind_host,e)})

