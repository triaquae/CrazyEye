#_*_coding:utf-8_*_


import subprocess

def run(host,port):
    cmd_str = "ssh alex@%s -p%s" %(host,port)
    cmd = subprocess.run(cmd_str,shell=True)

    print("---exec done-----")




# run("10.211.55.5",22)

