# CrazyEye
OpenSource IT Automation Software



CrazyEye介绍
==================
CrazyEye是基于Python开发的一款简单易用的IT管理软件，目前主要具体以下功能：

- 运维审计
   - 支持主机分组管理
   - 可为运维人员分配指定服务器、指定账号的操作权限
   - 运维人员的所有操作均可被记录下来以供日后审计

- 主机批量操作
   - 可对指定数量的机器进行批量命令、文件分发操作，可实时查看操作进度和结果

注意:: 目前暂时不支持对Windows系统的操作审计和批量任务


下载
========

`$ git clone https://github.com/triaquae/CrazyEye.git`


Docker 版
================

CrazyEye同时提供了Docker集成版本，直接执行下面步骤即可开始使用CrazyEye 

`$ git clone https://github.com/triaquae/CrazyEye.git`

`$ cd CrazyEye/crazyeye_docker `

`$ docker-compose up -d` #启动crazyeye的docker container 

`$ docker ps` #查看已启动的containers,找到crazyeye_nginx 对应的container id(输出内容的第一列)

`$ docker exec -ti <上面的container id> /bin/bash ` #这条命令会带你进入一个已经启动的container

`$ /opt/CrazyEye/manage.py createsuperuser` #这条命令是创建管理员账号，创建完成后，就可以通过浏览器访问`http://your_host_addr:8000/admin` 输入你刚创建的管理账户的用户名密码，就可以开始配置CrazyEye啦，详情看`http://crazyeyedoc.readthedocs.org/en/latest/#id3` 

*注意：如果想通过SSH登录，则需要`ssh crazyeye@<你docker container所运行的机器> -p8022`, 密码是`crazyeye`, 连接上后会提示你输入token,这个可以直接按回车，然后会要求你输入username 和password, 这时输入你自己的管理员账号就可以啦。


普通安装
==================

请看详细安装文档: http://crazyeyedoc.readthedocs.org/en/latest/#


Live Demo
=============

Demo 地址: #有木有人愿意捐赠个虚拟主机来跑demo? 哈哈

username:

password:


作者介绍
=============

Alex,多年运维+自动化开发经验,曾任职公安部、飞信、Nokia中国、中金公司、Advent软件、汽车之家等公司,目前任老男孩教育Python教学总监，热爱技术、电影、音乐、旅游、妹子！

他的Python教学视频 http://edu.51cto.com/lecturer/user_id-3050674.html


技术支持
=============

目前CrazyEye发布是的1.0测试版,由于时间有限，在使用过程中难免会出现一些小bug,你可以加入 `CrazyEye官方支持QQ群(29215534)` 提交bug,我会尽快回复！
