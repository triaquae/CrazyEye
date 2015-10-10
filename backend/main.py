#_*_coding:utf-8_*_
__author__ = 'jieli'
import sys
import ssh_interactive
import db_conn
from CrazyEye import settings
from web import models
from django.contrib import auth
import datetime
import django
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction

def call(sys_args):

    if len(sys_args) == 0:
        feature_list()
    else:
        feature_ins = Features()
        if hasattr(feature_ins, sys_args[0]):
            func = getattr(feature_ins,sys_args[0])
            func(sys_args)
        else:
            print "\033[31;1mInvalid argument!\033[0m"
            feature_list()
def feature_list():
    features = '''
    run     run audit interactive interface
    help    show helps
    '''
    print(features)

def print_msg(msg,msg_type,exit=False):
    if msg_type == 'err':
        print  "\033[31;1m%s\033[0m" % msg
    elif msg_type == 'normal':
        print  "\033[32;1m%s\033[0m" % msg
    elif msg_type == 'warning':
        print  "\033[33;1m%s\033[0m" % msg
    if exit:
        sys.exit()
class Features(object):

    def __init__(self):
        self.cmd_logs = []
        self.django_settings = settings

    def run(self,argv):

        self.token_auth()
        if  self.__auth():
            print(settings.Welcome_msg)
            self.__user_interactive()
    def __user_interactive(self):
        self.fetch_hosts()
    def token_auth(self):
        count = 0
        while count <3:
            token = raw_input("press ENTER if you don't have token, [input your token]:").strip()
            if len(token) == 0:return None
            filter_date = datetime.timedelta(seconds=-300)
            token_list = models.Token.objects.filter(token=token,date__gt=django.utils.timezone.now() +filter_date)
            if len(token_list) >0:
                if len(token_list) >1:
                    print "Found more than 1 matched tokens,I cannot let you login,please contact your IT guy!"
                else: #auth correct
                    bind_host_obj = token_list[0].host
                    self.login_user = token_list[0].user.user
                    self.user_id = token_list[0].user.user.id

                    print_msg("--- logging host[%s@%s(%s)], be patient,it may takes a minute --- " %(bind_host_obj.host_user.username,bind_host_obj.host.hostname,bind_host_obj.host.ip_addr),'normal')
                    try:
                        ssh_interactive.login(self,bind_host_obj)
                        print_msg('Bye!','warning',exit=True)
                    except Exception,e:
                        print e
                    finally:
                        self.flush_audit_log(bind_host_obj)
            else:
                count +=1
                print "Invalid token,got %s times to try!" % (3-count)
        else:
            sys.exit("Invalid token, too many attempts,exit.")


    def __auth(self):
       import getpass
       count = 0
       while count < 3:
            user = raw_input("Username:").strip()
            passwd = getpass.getpass("Password:")
            if len(user) == 0 or len(passwd) == 0:
                print "Username or password cannot be empty!"
                continue

            user = auth.authenticate(username=user, password=passwd)
            try:
                if user is not None: #pass authentication
                    if django.utils.timezone.now() > user.userprofile.valid_begin_time and django.utils.timezone.now() < user.userprofile.valid_end_time:
                        self.login_user = user
                        self.user_id = user.id
                        return True
                    else:
                        sys.exit("\033[31;1mYour account is expired,please contact your IT guy for this!\033[0m")
                else:
                    print "\033[31;1mInvalid username or password!\033[0m"
                    count +=1
            except ObjectDoesNotExist:
                sys.exit("\033[31;1mhaven't set CrazyEye account yet ,please login http://localhost:8000/admin find 'CrazyEye账户' and create an account first!\033[0m")
       else:
           sys.exit("Invalid username and password, too many attempts,exit.")

    #def fetch_hosts(self):

    def fetch_hosts(self):
        host_groups = list(self.login_user.userprofile.host_groups.select_related())

        while True:
            try:

                print 'z. Ungrouped [%s]' % self.login_user.userprofile.bind_hosts.select_related().count()
                for index,h_group in enumerate(host_groups):
                    #host_list = models.BindHosts.objects.filter(host_group__id=h_group.id)
                    host_list = h_group.bindhosts_set.select_related()
                    print '%s. %s [%s]' % (index, h_group.name,len(host_list))



                user_choice = raw_input("\033[32;1m>>:\033[0m").strip()

                if user_choice.isdigit():
                    user_choice = int(user_choice)
                    if user_choice < len(host_groups):
                        while True:
                            hosts = models.BindHosts.objects.filter(host_group__id=host_groups[user_choice].id )
                            for index,h in enumerate(hosts):
                                print "  %s.\t%s(%s)  %s" %(index,h.host.hostname,h.host.ip_addr,h.host_user.username)
                            user_choice2 = raw_input("\033[32;1m['b'(back)]>>>:\033[0m").strip()

                            if user_choice2.isdigit():
                                user_choice2 = int(user_choice2)
                                if user_choice2 <len(hosts):
                                    h= hosts[user_choice2]
                                    print '\033[32;1m-----connecting [%s] with user [%s]-----\033[0m' %(h.host.ip_addr,h.host_user.username)
                                    try:
                                        ssh_interactive.login(self,h)
                                    except Exception,e:
                                        print "\033[31;1m%s\033[0m" %e
                                    finally:
                                        self.flush_audit_log(h)
                                else:
                                    print_msg("No this option!", 'err')
                            elif user_choice2 == 'b':
                                break

                    else:
                        print_msg("No this option!", 'err')
                elif user_choice == 'z': #for ungrouped hosts
                    hosts = self.login_user.userprofile.bind_hosts.select_related()
                    while True:
                        for index,h in enumerate(hosts):
                            print "  %s.\t%s(%s)  %s" %(index,h.host.hostname,h.host.ip_addr,h.host_user.username)
                        user_choice2 = raw_input("\033[32;1m['b'(back)]>>>:\033[0m").strip()

                        if user_choice2.isdigit():
                            user_choice2 = int(user_choice2)
                            if user_choice2 <len(hosts):
                                h= hosts[user_choice2]
                                print '\033[32;1m-----connecting [%s] with user [%s]-----\033[0m' %(h.host.ip_addr,h.host_user.username)
                                try:
                                    ssh_interactive.login(self,h)
                                except Exception,e:
                                    print "\033[31;1m%s\033[0m" %e
                                finally:
                                    self.flush_audit_log(h)
                            else:
                                print_msg("No this option!", 'err')
                        elif user_choice2 == 'b':
                            break


                elif user_choice == 'exit':
                    print_msg('Bye!','warning',exit=True)
            except (KeyboardInterrupt,EOFError):
                print_msg("input 'exit' to logout!",'err')
            except UnicodeEncodeError,e:
                print_msg("%s, make sure you terminal supports utf8 charset!" % str(e),'err',exit=True)
    def flush_cmd_input(self,log,host,action_type):
        current_time = django.utils.timezone.now()
        self.cmd_logs.append([current_time,log,action_type])
        if action_type == 1: #new login session,create session track id first
            self.session_track = models.SessionTrack()
            self.session_track.save()
        if action_type == 2:
            self.session_track.closed = True
            self.session_track.save()
        if len(self.cmd_logs)>10:
            self.flush_audit_log(host)

    @transaction.atomic
    def flush_audit_log(self,h):

        for log in self.cmd_logs:

            row = models.AuditLog(
                    session = self.session_track,
                    user = self.login_user.userprofile,
                    host = h,
                    action_type = log[2],
                    cmd = log[1],
                    date =  log[0]
                )
            row.save()
        self.cmd_logs =[]
        return True