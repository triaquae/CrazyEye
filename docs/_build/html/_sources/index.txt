



.. CrazyEye documentation master file, created by
   sphinx-quickstart on Thu Oct  1 11:28:16 2015.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

CrazyEye介绍
==================
CrazyEye是基于Python开发的一款简单易用的IT管理软件，目前主要具体以下功能：

- 运维审计
   - 支持主机分组管理
   - 可为运维人员分配指定服务器、指定账号的操作权限
   - 运维人员的所有操作均可被记录下来以供日后审计

- 主机批量操作
   - 可对指定数量的机器进行批量命令、文件分发操作，可实时查看操作进度和结果

.. warning:: 目前暂时不支持对Windows系统的操作审计和批量任务



安装
==================

在安装CrazyEye前请确保你的Linux系统的Python版本是2.7+,Python3.0+还未做过测试,请谨慎使用

CrazyEye安装所需要的组件：

- Django 1.8+
- Paramiko 最新版本
- Django suite
- Shellinabox
- Mysql
- Python 连接Mysql的模块


开始安装

1. 安装Django,Paramiko,Django-suite,MySQL-python

.. code-block:: shell


   pip install Django==1.8.4

   pip install django-suit==0.2.15

   pip install paramiko

   #安装python连接mysql的模块
   yum install MySQL-python  #for CentOS
   pip install MySQL-python  #for Ubuntu

2. 安装Shellinabox

   从此处下载 https://code.google.com/p/shellinabox/downloads/list

   解压下载包进入shellinabox源码目录，进行编译安装

.. code-block:: shell


    ./configure
    make && makeinstall


3. 安装CrazyEye

   下载最新版CrazyEye源码并解压后，编辑主配置文件
   :code:`CrazyEye/settings.py`, 在此配置文件中配置好与Mysql数据库的连接


.. code-block:: python

   # Database
   # https://docs.djangoproject.com/en/1.8/ref/settings/#databases

   DATABASES = {
       'default': {
           'ENGINE': 'django.db.backends.mysql',
           'NAME': 'CrazyEyes',  #需要你自己在你的mysql数据库中先创建好该数据库
           'HOST': '',  #如果数据库在远程的机器上，此处填写远程数据库服务器的IP
           'PORT':3306,
           'USER':'root',
           'PASSWORD': ''  #为空代表没密码
       }
   }


4. 配置Mysql数据库支持中文

   打开mysql 数据库配置文件，分别在[mysqld]和[client]部分添加以下内容:

.. code-block:: shell

   [mysqld]
   character-set-server=utf8
   ...

   [client]
   default-character-set=utf8
   #注意，修改完配置后需要重启Mysql服务后才能生活噢！



5. 在主目录执行以下命令来初始化CrazyEye的数据库表结构：

.. code-block:: python

   python manage.py makemigrations
   python manage.py migrate

   python manage.py createsuperuser #创建管理员用户


6. 创建一个审计用户 :code:`crazy_audit` ,并在此用户的 :code:`.bashrc` 用户环境变量文件的最底部，加上以下两条代码：

.. code-block:: shell
   :emphasize-lines: 13,14,15

   useradd crazy_audit

   su - crazy_audit
   vi .bashrc
   #在尾部添加以下2行代码：
   python /YourCrazyEyeInstallPath/CrazyEye/crazy_eyes_mgr.py run
   logout

   #此时crazy_audit用户的环境变量配置文件 看上去如下
   more /home/crazy_audit/.bashrc
   ...
   ...
   python /YourCrazyEyeInstallPath/CrazyEye/crazy_eyes_mgr.py run   #把YourCrazyEyeInstallPath替换成你自己的软件安装目录
   logout

   #用ssh登录到此用户，在输入用户名密码后，如果显示以下提示，则代表配置成功

   press ENTER if you don't have token, [input your token]: #此处敲回车
   Username:
   Password:


7. 启动WEB登录页面

   :code:`python manage.py runserver 0.0.0.0:8000`, 然后在浏览器输入此地址:code:`http://localhost:8000/admin`,输入你刚才创建的管理员用户名和密码

   .. image:: _static/imgs/crazy_eye_admin_login.png


恭喜！你已成功安装了CrazyEye,现在可以开始配置使用了！

配置CrazyEye
==================

- :ref:`创建主机`
- :ref:`创建远程用户`
- :ref:`创建主机与远程用户绑定关系`
- :ref:`创建CrazyEye账户`
- :ref:`配置WebSSH`
- :ref:`设置批量任务最大并发数`
- :ref:`配置WebSSH`



部署到生产环境
=============

CrazyEye默认是以测试环境运行的，在测试环境下，所有的功能虽然和生产环境模式都是一样的，但是却是不能支持多并发的，因为CrazyEye所依赖的Django WEB服务器是单线程的，So如果想让CrazeEye支持高并发，需要借助Apachel或Nginx Web服务器，我们建议你使用Nginx来做CrazyEye的高并发。

若想让nginx支持Django web服务，需要借助一个第三方Python模块叫uwsgi,具体安装和配置nginx支持Django的方法请参考uwsgi官方文档！

Uwsgi文档: http://uwsgi-docs.readthedocs.org/en/latest/tutorials/Django_and_nginx.html



ScreenShots
============

- :ref:`ScreenShots`

Live Demo
=============

Demo 地址:

username:

password:


作者介绍
=============

Alex,多年运维+自动化开发经验,曾任职公安部、飞信、Nokia中国、中金公司、Advent软件、汽车之家等公司,目前任老男孩教育Python教学总监，热爱技术、电影、音乐、旅游、妹子！

.. note:: 他的Python教学视频 http://edu.51cto.com/lecturer/user_id-3050674.html

.. image:: _static/imgs/author_pic.jpg

技术支持
=============

目前CrazyEye发布是的1.0测试版,由于时间有限，在使用过程中难免会出现一些小bug,你可以加入 :code:`CrazyEye官方支持QQ群(29215534)` 提交bug,我会尽快回复！