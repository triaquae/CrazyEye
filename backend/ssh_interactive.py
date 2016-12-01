#!/usr/bin/env python

# Copyright (C) 2003-2007  Robey Pointer <robeypointer@gmail.com>
#
# This file is part of paramiko.
#
# Paramiko is free software; you can redistribute it and/or modify it under the
# terms of the GNU Lesser General Public License as published by the Free
# Software Foundation; either version 2.1 of the License, or (at your option)
# any later version.
#
# Paramiko is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more
# details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with Paramiko; if not, write to the Free Software Foundation, Inc.,
# 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA.


import base64
from binascii import hexlify
import getpass
import os
import select
import socket
import sys
import time
import traceback
from paramiko.py3compat import input
import termios
import signal
import fcntl
import struct
import paramiko
import subprocess
from backend import  utils
from backend import audit
try:
    import interactive
except ImportError:
    from . import interactive


def agent_auth(transport, username):
    """
    Attempt to authenticate to the given transport using any of the private
    keys available from an SSH agent.
    """
    
    agent = paramiko.Agent()
    agent_keys = agent.get_keys()
    if len(agent_keys) == 0:
        return
        
    for key in agent_keys:
        print('Trying ssh-agent key %s' % hexlify(key.get_fingerprint()))
        try:
            transport.auth_publickey(username, key)
            print('... success!')
            return
        except paramiko.SSHException:
            print('... nope.')


def manual_auth(ins,username, hostname,pw,host_obj,main_ins):

    #auth = input('Auth by (p)assword, (r)sa key, or (d)ss key? [%s] ' % default_auth)

    if host_obj.host_user.auth_method == 'ssh-key':
        #default_path = os.path.join(os.environ['HOME'], '.ssh', 'id_rsa')
        #path = input('RSA key [%s]: ' % default_path)
        #if len(path) == 0:
        path = main_ins.django_settings.RSA_PRIVATE_KEY_FILE

        if not os.path.isfile(path):
            sys.exit("\033[31;1mError:RSA private key file [%s] doesn't exist, please make sure you have set your RSA correctly.\033[0m" % path )
        try:
            key = paramiko.RSAKey.from_private_key_file(path)

        except paramiko.PasswordRequiredException:
            password = getpass.getpass('RSA key password: ')
            key = paramiko.RSAKey.from_private_key_file(path, password)
        ins.auth_publickey(username, key)

    else:
        ins.auth_password(username, pw)


# setup logging
#paramiko.util.log_to_file('demo.log')
def get_session_id(instance,bind_host_obj,tag):
    '''apply  session id'''
    session_obj = instance.models.Session(user_id = instance.login_user.id,bind_host=bind_host_obj,tag=tag)

    session_obj.save()
    #print('session id:', session_obj)
    return session_obj


def login_raw(instance,h):
    '''invoke native ssh client'''

    ip, port, username, password = h.host.ip_addr, h.host.port, h.host_user.username, h.host_user.password
    ssh_path = instance.django_settings.SSH_CLIENT_PATH
    rand_tag_id = utils.random_str(16)
    session_obj = get_session_id(instance,h,rand_tag_id)
    session_track_process = subprocess.Popen(
        "/bin/sh %s/backend/session_tracker.sh %s  %s" % (instance.django_settings.BASE_DIR,session_obj.id,rand_tag_id),
        shell=True,
        cwd= instance.django_settings.BASE_DIR,
        stdout=subprocess.PIPE,
        stderr= subprocess.PIPE
    )
    cmd_str = "sshpass -p %s %s %s@%s -p%s -Z %s" %(password,ssh_path,username,ip,port , rand_tag_id)

    subprocess.run(cmd_str,shell=True)

    #print('---login done--',rand_tag_id, session_track_process.poll())
    # if session_track_process.poll() is not None:
    #     print("stdout:",session_track_process.stdout.read())
    #     print("stderr:",session_track_process.stderr.read())

    #update session stay time
    session_obj.stay_time = time.time() -  session_obj.date.timestamp()
    session_log_file = "%s/%s/session_%s.log" %(instance.django_settings.SESSION_AUDIT_LOG_DIR,
                                    session_obj.date.strftime( "%Y_%m_%d"),
                                    session_obj.id
                                    )
    log_parser = audit.AuditLogHandler(session_log_file)
    log_data = log_parser.parse()
    session_obj.cmd_count = len(log_data)
    session_obj.save()

def login(main_ins,h):
    ip,port,username,password=h.host.ip_addr,h.host.port,h.host_user.username,h.host_user.password
    # now connect
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(15)
        sock.connect((ip, port))
    except Exception as e:
        print('*** Connect failed: ' + str(e))
        main_ins.flush_cmd_input(str(e),h,1)
        main_ins.flush_cmd_input('--session closed--',h,2)

        #traceback.print_exc()
        return #sys.exit(1)

    try:
        t = paramiko.Transport(sock)
        try:
            t.start_client()
        except paramiko.SSHException:
            print('*** SSH negotiation failed.')
            sys.exit(1)

        try:
            keys = paramiko.util.load_host_keys(os.path.expanduser('~/.ssh/known_hosts'))
        except IOError:
            try:
                keys = paramiko.util.load_host_keys(os.path.expanduser('~/ssh/known_hosts'))
            except IOError:
                #print('*** Unable to open host keys file')
                keys = {}


        agent_auth(t, username)
        if not t.is_authenticated():
            manual_auth(t, username, ip,password,h,main_ins)
        if not t.is_authenticated():
            print('*** Authentication failed. :(')
            t.close()
            sys.exit(1)

        chan = t.open_session()
        t_height,t_width = get_terminal_size()
        chan.get_pty(term='xterm',height=t_height,width=t_width)
        chan.invoke_shell()
        print('*** Login success ***\n')
        main_ins.flush_cmd_input('---- Logged in! ----',h,1)
        main_ins.flush_audit_log(h)
        try:
            signal.signal(signal.SIGWINCH, get_terminal_size)
        except:
            pass


        interactive.interactive_shell(chan,main_ins,ip,username,h)
        chan.close()
        t.close()

    except Exception as e:
        print('\033[31;1m%s\033[0m' % str(e))
        main_ins.flush_cmd_input(str(e),h,1)
        main_ins.flush_cmd_input('--session closed--',h,2)

        #traceback.print_exc()
        try:
            t.close()
        except:
            pass
        #sys.exit(1)



def get_terminal_size():
    """Returns a tuple (x, y) representing the width(x) and the height(x)
    in characters of the terminal window."""
    def ioctl_GWINSZ(fd):
        try:
            import fcntl, struct
            cr = struct.unpack('hh', fcntl.ioctl(fd, termios.TIOCGWINSZ,
        '1234'))
        except:
            return None
        return cr
    cr = ioctl_GWINSZ(0) or ioctl_GWINSZ(1) or ioctl_GWINSZ(2)
    if not cr:
        try:
            fd = os.open(os.ctermid(), os.O_RDONLY)
            cr = ioctl_GWINSZ(fd)
            os.close(fd)
        except:
            pass
    if not cr:
        try:
            cr = (env['LINES'], env['COLUMNS'])
        except:
            cr = (25, 80)
    return int(cr[1]), int(cr[0])


def get_terminal_size():
    """
    get terminal size
    """
    if 'TIOCGWINSZ' in dir(termios):
        TIOCGWINSZ = termios.TIOCGWINSZ
    else:
        TIOCGWINSZ = 1074295912
    s = struct.pack('HHHH', 0, 0, 0, 0)
    x = fcntl.ioctl(sys.stdout.fileno(), TIOCGWINSZ, s)
    return struct.unpack('HHHH', x)[0:2]

if __name__ == '__main__':
    #login('192.168.2.250', 22,'alex','alex3714')
    print(get_terminal_size())