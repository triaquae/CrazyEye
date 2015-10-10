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


import socket
import sys
from paramiko.py3compat import u

unsupport_cmd_list = ['rz','sz']

# windows does not have termios...
try:
    import termios
    import tty
    import time
    has_termios = True
except ImportError:
    has_termios = False

#interactive.interactive_shell(chan,main_ins,host_ip,username)
def interactive_shell(chan,main_ins,host_ip,username,host_ins):
    if has_termios:
        #print '--->posix:', main_ins.login_user,host_ip,username
        posix_shell(chan,main_ins,host_ip,username,host_ins) #unix shell
    else:
        windows_shell(chan)


def posix_shell(chan,self,host_ip,username,host_ins):
    import select
    
    oldtty = termios.tcgetattr(sys.stdin)
    try:
        tty.setraw(sys.stdin.fileno())
        tty.setcbreak(sys.stdin.fileno())
        chan.settimeout(0.0)


        cmd = ''
        tab_input_flag = False
        while True:
            r, w, e = select.select([chan, sys.stdin], [], [])

            if chan in r:
                try:

                    x = u(chan.recv(1024))
                    if tab_input_flag:
                        cmd +=''.join(x[:10])
                        tab_input_flag = False
                    if len(x) == 0:
                        sys.stdout.write('\r\n\033[32;1m*** Session Closed ***\033[0m\r\n')
                        self.flush_cmd_input('*** Session Closed ***',host_ins,2)
                        break

                    sys.stdout.write(x)
                    sys.stdout.flush()

                except socket.timeout:
                    pass
                except UnicodeDecodeError,e:
                    pass         
            if sys.stdin in r:
                x = sys.stdin.read(1)
                if len(x) == 0:
                    break
                if not x == '\r':
                    cmd +=x
                else:
                    if len(cmd.strip())>0:
                        self.flush_cmd_input(cmd,host_ins,0)
                    if cmd in unsupport_cmd_list:
                        x="...Operation is not supported!\r\n"
                    cmd=''

                if x == '\t':
                    tab_input_flag = True
                chan.send(x)

        #f.close()
        #print cmd_list
    finally:
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, oldtty)

    
# thanks to Mike Looijmans for this code
def windows_shell(chan):
    import threading

    sys.stdout.write("Line-buffered terminal emulation. Press F6 or ^Z to send EOF.\r\n\r\n")
        
    def writeall(sock):
        while True:
            data = sock.recv(256)
            if not data:
                sys.stdout.write('\r\n\033[32;1m*** Session closed ***\033[0m\r\n\r\n')
                sys.stdout.flush()
                break
            sys.stdout.write(data)
            sys.stdout.flush()
        
    writer = threading.Thread(target=writeall, args=(chan,))
    writer.start()
        
    try:
        while True:
            d = sys.stdin.read(1)
            if not d:
                break
            chan.send(d)
    except EOFError:
        # user hit ^Z or F6
        pass
