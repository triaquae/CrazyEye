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


Docker Version
================

CrazyEye同时提供了Docker集成版本，直接执行下面步骤即可开始使用CrazyEye 

`$ git clone https://github.com/triaquae/CrazyEye.git`

`$ cd CrazyEye/crazyeye_docker `

`$ docker-compose up -d` #启动crazyeye的docker container 
下载docker image后执行 `docker run -ti --name crazyeye -p 8000:8000 -p 8022:22 -p 4200:4200 alex3714/crazyeye /CrazyEye/crazyeye_run.sh` 

然后即可访问`http://your_host_addr:8000` 登录crayzye,  用户名密码均为`admin` 

安装
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
