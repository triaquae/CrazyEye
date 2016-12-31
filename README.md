# CrazyEye
OpenSource IT Automation Software



CrazyEye介绍
==================
CrazyEye是基于Python开发的一款简单易用的IT审计堡垒机,通过对原生ssh代码进行了部分修改，从而实现用户在登录堡垒机后，他所有的命令操作都将被实时抓取并写入审计日志，以供后期审计，目前CrazyEye主要实现了以下功能：

- 用户行为审计
   - 支持对主机进行分组管理
   - 可为运维人员分配指定服务器、指定账号的操作权限，即一个用户可以登录多少生产服务器，以及登录后有什么权限，都可以自如的控制
   - 用户登录堡垒后的所有操作均可被记录下来以供日后审计.

- 主机批量操作
   - 可对指定数量的机器进行批量命令、文件分发操作，可实时查看操作进度和结果

注意:: 目前暂时不支持对Windows系统的操作审计和批量任务


快速安装`(for Ubuntu)`
========
###环境依赖

    python3.5+
    
    cryptography==1.5.2
    Django==1.10.2
    django-session-security==2.4.0
    djangorestframework==3.5.3
    paramiko==2.0.2
    pycparser==2.16
    PyMySQL==0.7.9
    
    
    sshpass 
    openssh
    


###1.下载CrazyEye
`$ git clone https://github.com/triaquae/CrazyEye.git`

###2.安装python环境依赖

*  首先确保使用的python版本是3.5+
*  进入CrazyEye目录执行`sudo pip3 install -r requirements.txt `

####3.安装sshpass
*  进入src目录,执行`tar xvzff sshpass-1.06.tar.gz`
*  `cd sshpass-1.06/`
*  `./configure`
*  `make && make install`


###3.安装改过源码的openssh 
* `cd src/openssh-7.3p1/`
*  `./configure --prefix=/usr/local/openssh7/ `
 
    注意有可能会报错误configure: error: OpenSSL version header not found.这是因为openssh需要openssl,此时需要安装一下openssl的开发模块` 
    
        在ubuntu上安装openssl dev组件
        sudo apt-get install zlib1g
        sudo apt-get install zlib1g-dev
        sudo apt-get install libssl-dev
        
        再重新执行configure就应该没问题了

*  `make && make install`

###4.配置审计用户 
*   创建一个审计用户,`adduser crazy_audit`
*   修改audit_user的.bashrc， `vim /home/crazy_audit/.bashrc`,在文件末尾加下以下2行并保存

        python3 /usr/local/CrazyEye/crazy_eyes_mgr.py run
        
        logout

* 修改sudo配置文件，使crazy_audit用户可以在sudo时不用输入密码
  
    $ sudo vim /etc/sudoers
    
        %crazy_audit    ALL=NOPASSWD:ALL #/usr/bin/strace,/usr/bin/python3


###5.启动CrazyEye


    sudo python3 manage.py runserver 0.0.0.0:9000
    *注意启动此程序的用户不应是crazye_audit用户
    

###6.登录
*   管理用户登录通过浏览器打开`http://your_ip_addr:9000/`
    
        用户名:alex@126.com
        密码: alex3714 


*  普通只需要通过命令行登录即可 
 
        Alexs-MacBook-Pro:~ alex$ ssh crazy_audit@10.211.55.5
        crazy_audit@10.211.55.5's password: *此处填写你之前创建的crazy_audit的密码
        
        press ENTER if you don't have token, [input your token]: #敲回车就行
        Username:alex@126.com #此处方是真正的你为用户创建的审订账号
        Password:
        
        |-------[Welcome login CrazyEye Auditing System]-----|
        |            Version :   1.0                         |
        |            Author  :   Alex Li                     |
        |            QQ Group:   29215534                    |
        |----------------------------------------------------|
        
        
        z. Ungrouped [3] #你授权这个用户可以访问的主机列表 
        >>:z
          0.	ubuntu(10.211.55.5)  alex
          1.	oldboy web server 错的(202.106.23.22)  Alex
          2.	oldboy web server(101.200.195.98)  Alex
        ['b'(back)]>>>:0 #选中一台机器登录
        -----connecting [10.211.55.5] with user [alex]-----
        sshpass -p alex3714 /usr/local/openssh7v2/bin/ssh alex@10.211.55.5 -p22 -Z hrqdan3soljbux6t -o StrictHostKeyChecking=no
        session_tag: hrqdan3soljbux6t
        Welcome to Ubuntu 16.04 LTS (GNU/Linux 4.4.0-53-generic x86_64)
        
         * Documentation:  https://help.ubuntu.com/
        
        313 packages can be updated.
        26 updates are security updates.
        
        Last login: Sat Dec 31 15:39:59 2016 from 10.211.55.5
        alex@alex-ubuntu:~$ ifconfig #登录上了远程机器了
        enp0s5    Link encap:Ethernet  HWaddr 00:1c:42:2d:c0:18  
                  inet addr:10.211.55.5  Bcast:10.211.55.255  Mask:255.255.255.0
                  inet6 addr: fdb2:2c26:f4e4:0:3c28:9879:d171:74be/64 Scope:Global
                  inet6 addr: fe80::8a5e:4c84:4dbb:5e3/64 Scope:Link
                  inet6 addr: fdb2:2c26:f4e4:0:e59a:3d73:452b:1dc7/64 Scope:Global
                  UP BROADCAST RUNNING MULTICAST  MTU:1500  Metric:1
                  RX packets:26899 errors:0 dropped:0 overruns:0 frame:0
                  TX packets:17202 errors:0 dropped:0 overruns:0 carrier:0
                  collisions:0 txqueuelen:1000 
                  RX bytes:13283203 (13.2 MB)  TX bytes:5233012 (5.2 MB)
        
        lo        Link encap:Local Loopback  
                  inet addr:127.0.0.1  Mask:255.0.0.0
                  inet6 addr: ::1/128 Scope:Host
                  UP LOOPBACK RUNNING  MTU:65536  Metric:1
                  RX packets:24016 errors:0 dropped:0 overruns:0 frame:0
                  TX packets:24016 errors:0 dropped:0 overruns:0 carrier:0
                  collisions:0 txqueuelen:1 
                  RX bytes:4440146 (4.4 MB)  TX bytes:4440146 (4.4 MB)
        
        alex@alex-ubuntu:~$ 
        alex@alex-ubuntu:~$ 
        alex@alex-ubuntu:~$ ls
        a.py      Desktop    Downloads         Music          Pictures  ssh_log   Templates  test.zip
        CrazyEye  Documents  examples.desktop  openssh-7.3p1  Public    ssh_log2  test.py    Videos
        alex@alex-ubuntu:~$ pwd
        /home/alex
        alex@alex-ubuntu:~$ exit #退出这台机器 
        logout
        Connection to 10.211.55.5 closed.  #又回到审计交互界面
          0.	ubuntu(10.211.55.5)  alex
          1.	oldboy web server 错的(202.106.23.22)  Alex
          2.	oldboy web server(101.200.195.98)  Alex
        ['b'(back)]>>>:b
        z. Ungrouped [3]
        >>:exit #即出审计系统 
        Bye!
        Connection to 10.211.55.5 closed. 




作者介绍
=============

Alex,多年IT自动化开发经验,国内PYTHON语言知名推广者，曾任职公安部、飞信、Nokia中国、中金公司、Advent软件、汽车之家等公司,目前任老男孩教育Python教学总监，热爱抽烟、喝酒、烫头！

他的Python教学视频 http://study.163.com/course/courseMain.htm?courseId=1003245008


技术支持
=============

目前CrazyEye发布是的1.0测试版,由于时间有限，在使用过程中难免会出现一些小bug,你可以加入 `PYTHON开发交流QQ群(29215534)` 提交bug,我会尽快回复！
