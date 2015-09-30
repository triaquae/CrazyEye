#_*_coding:utf-8_*_
__author__ = 'jieli'

import  multiprocessing
import paramiko

class MultiTask(object):
    '''handles all the multi task works'''
    def __init__(self,main_ins):
        self.main_ins = main_ins
        self.cmd_dic = {
            'help' : self.__show_cmd_list,
            'run_cmd': self.__run_cmd,
        }

    def interactive(self):
        '''invoke features according to user's input'''
        while True:
            try:
                raw_instruction = raw_input("\033[33;1m[spawn mode]:\033[0m").strip()
                if len(raw_instruction) == 0:continue
                elif raw_instruction[0] == 'exit':break
                instruction = raw_instruction.split()
                if self.cmd_dic.has_key(instruction[0]):
                    func = self.cmd_dic[instruction[0]]
                    func(instruction)
                else:
                    print "\033[31;1mWrong cmd usage,enter help to see cmd list\033[0m"
            except (KeyboardInterrupt,EOFError):
                print '\n'
                break
    def __show_cmd_list(self,msg):
        '''show all available cmd list'''
        help_content = '''
        run_cmd     run cmd on multiple hosts
                    run_cmd -u remote_user -g group1,group2 -cmd pwd
                    run_cmd -u remote_user -re regular expression -cmd pwd
        '''
        print help_content
    def __run_cmd(self,msg):

        if self.__parse_argv(msg):
            task_host_list = self.__fetch_hosts(msg)
            if task_host_list:
                while True:
                    user_choice = raw_input("Are you sure you want to run [\033[33;1m%s\033[0m] command on above hosts？（Y/N）" % msg[msg.index('-cmd')+1]).strip()
                    if len(user_choice) == 0:continue
                    if user_choice == 'Y' or user_choice == 'y':

                        self.__multi_run_mgr(task_host_list,msg[msg.index('-cmd')+1])
                        break
                    elif user_choice == 'N' or user_choice == 'n':
                        print "\033[33;1mTask canceled!\033[0m"
                        break
    def __fetch_hosts(self,msg):
        '''fetch hosts from database according to user input'''
        remote_username = msg[msg.index('-u') +1]
        remote_users =self.main_ins.ms.select("select id,username,password from host_users where username=%s",(remote_username,))
        if not remote_users:
            print "\033[31;1mError:远程用户%s不存在\033[0m" % remote_username
            return

        if '-g' in msg:
            groups = msg[msg.index('-g')+1].split(',')
            group_ids = self.main_ins.ms.select("select id from groups where name in %s",(groups,))
            if not group_ids:
                print "\033[31;1mGroup %s doesn't exist in database." % groups
                return
            group_ids = [i[0] for i in group_ids]

            query_code = '''
              SELECT host_groups.id ,
                  host_groups.group_id ,
                  host_groups.user_id,
                  bind_hosts.host_id,
                  bind_hosts.host_user_id
              from host_groups,bind_hosts
              where host_groups.user_id =%s
              and host_groups.group_id in %s
              and host_groups.bind_host_id = bind_hosts.id;'''
            host_list = self.main_ins.ms.select(query_code,(self.main_ins.user_id,group_ids))

            host_ids = [i[3] for i in host_list]
            host_user_ids = [i[0] for i in remote_users]
            host_query_code = '''
                select hosts.id ,
                    hosts.ip ,
                    hosts.hostname ,
                    hosts.port ,
                    host_users.username ,
                    host_users.password
                from hosts,host_users,bind_hosts
                where hosts.id = bind_hosts.host_id
                and host_users.id = bind_hosts.host_user_id
                and bind_hosts.id in %s
                and host_users.username = %s'''
            host_detail_list = self.main_ins.ms.select(host_query_code,(host_ids,remote_username))
            if host_detail_list:
                print  '------matched hosts-------'
                for h in host_detail_list:
                    print '\t%s\t%s' %(h[1],h[2])
                print '\033[32;1m[%s] hosts matched!\033[0m' % len(host_detail_list)

                return host_detail_list
        elif '-re' in msg:
            all_avaliable_hosts_query = '''select user.username,
                hosts.ip,
                hosts.hostname,
                hosts.port ,
                host_users.username,
                host_users.`password`,
                groups.name
            from hosts,host_users,bind_hosts,host_groups,user,groups
            where bind_hosts.host_id = hosts.id
            and  bind_hosts.host_user_id = host_users.id
            and host_groups.bind_host_id = bind_hosts.id
            and host_groups.user_id = user.id
            and host_groups.group_id = groups.id
            and user.id = %s
            and host_users.username = %s '''
            all_avaliable_hosts = self.main_ins.ms.select(all_avaliable_hosts_query,(self.main_ins.user_id,remote_username))
            match_str = msg[msg.index('-re')+1]
            matched_hosts =  [i for i in all_avaliable_hosts  if match_str in i[1] or match_str in i[2]]
            if matched_hosts:
                print  '------matched hosts-------'
                print 'Hostname\tIP\t\tGroup'
                for h in matched_hosts:
                    print '%s\t%s\t%s' %(h[2],h[1],h[-1])
            print '\033[32;1m[%s] hosts matched!\033[0m' % len(matched_hosts)
            return matched_hosts

    def __file_transfer(self,msg):
        pass
    def __multi_run_mgr(self,host_list,cmd):
        pool = multiprocessing.Pool(processes=settings.MaxTaskProcesses)
        lock = multiprocessing.Manager().Lock()
        res_list = []
        for h in host_list:

            p = pool.apply_async(run_task, args=(h,cmd,lock))
            res_list.append(p)

        pool.close()
        pool.join()
        print '--------All task are finished!-------'

    def __parse_argv(self,msg):
        '''
        run_cmd -g group1,group2,group3 -u root -c your_cmd > output.log
        run_cmd -g group1,group2,group3 -u alex -c your_cmd
        run_cmd -re 'web*' -c your_cmd
        '''
        err_msg = []
        try:
            if len(msg) >1:
                if '-g' in msg or '-re' in msg:
                    if '-g' in msg:
                        if not len(msg[msg.index('-g'):]) >0 or msg[msg.index('-g') +1].startswith('-'):
                            err_msg.append('Error:参数-g后面必须指定主机组')
                    if '-re' in msg:
                        if not len(msg[msg.index('-re'):]) >0 or msg[msg.index('-re') +1].startswith('-'):
                            err_msg.append('Error:参数-re后面必须指定匹配规则')
                    if '-g' in msg and   '-re' in msg:
                        err_msg.append('Error:参数-g和-re不能同时使用')
                    if '-u' in msg:
                        if not len(msg[msg.index('-u'):]) >0 or msg[msg.index('-u') +1].startswith('-'):
                            err_msg.append('Error:参数-u后面必须指定远程执行用户')

                        if msg[0] == 'run_cmd':
                            if not '-cmd' in msg:
                                err_msg.append('Error:参数中必须包含-cmd 指定要在远程执行命令')
                            else:
                                if not len(msg[msg.index('-cmd'):]) >0 or msg[msg.index('-cmd') +1].startswith('-'):
                                    err_msg.append('Error:参数-cmd后面必须指定要执行的命令')
                        elif msg[0] == 'file_transfer':
                            if not '-put' in msg or not '-get' in msg:
                                err_msg.append('Error:参数中必须包含-put 或-get 指定要传输的文件')
                            else:
                                if '-put' in msg:
                                    if not len(msg[msg.index('-put'):]) >1 or msg[msg.index('-put') +2].startswith('-'):
                                        err_msg.append('Error:参数-put后面必须指定需要传送的文件')
                                    if '-get' in msg:
                                        if not len(msg[msg.index('-get'):]) >1 or msg[msg.index('-get') +2].startswith('-'):
                                            err_msg.append('Error:参数-get后面必须指定需要从远程下载的文件')
                            if  '-put' in msg and  '-get' in msg:
                                err_msg.append('Error:参数-put和-get不能同时使用')
                    else:
                        err_msg.append('Error:参数中必须包含-u 指定远程执行用户')
                else:
                    err_msg.append('Error:参数中必须包含-g或者-re')
            else:
                err_msg.append('Error:命令后面必须跟参数！')
        except Exception,e:
            err_msg.append('Error:未知错误%s,输入help查看命令帮助!' % e )
        if err_msg:
            for err in err_msg:
                print '\033[31;1m%s\033[0m' % err

        else:
            return True

def run_task(task_info,cmd,lock):

    host_id,ip,hostname,port,username,password = task_info[:6]

    s = paramiko.SSHClient()	#绑定实例
    s.load_system_host_keys()	#加载本机know host主机文件
    s.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        s.connect(ip,port,username,password,timeout=5)   #连接远程主机
        stdin,stdout,stderr = s.exec_command(cmd)   #执行命令

        cmd_result = stdout.read(),stderr.read()    #读取命令结果

        lock.acquire()
        print '----------- HOST:%s  IP:%s -------------' %(hostname,ip)
        for line in cmd_result:
            print line,
        lock.release()
        s.close()
    except Exception,e:
        print '----------- HOST:%s  IP:%s -------------' %(hostname,ip)
        print '\033[31;1mError:%s\033[0m' % e