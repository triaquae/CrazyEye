#!/usr/bin/env python
# _*_coding:utf-8_*_
from __future__ import division
import re
import time
import os
import sys


class Person:
    def __init__(self, name=None, age=None, skill=['linux'], salary=None, balance=2000, love_heat=1):  # 定义构造函数
        self.name = name  # 定义角色名字
        self.age = age    # 定义角色年龄
        self.skill = skill  # 定义角色技能
        self.salary = salary # 定义角色工资
        self.balance = balance  # 定义角色存款
        self.love_heat = love_heat  # 定义角色爱情指数

    def input_info(self):   # 定义用户信息方法
        while True:
            input_name = raw_input('姓名:').strip()  # 输入用户名
            if len(input_name) == 0:
                continue
            else:
                self.name = input_name
                break
        while True:
            age = raw_input('年龄:').strip()  # 输入年龄
            if len(age) == 0 or len(age) > 2:  # 判断输入长度
                print '请输入有效数字！'
                continue
            try:
                pattern_age = re.compile('[0-9]{2}')
                result_age = re.search(pattern_age,age).group()  # 匹配输入获取输入结果
                if int(result_age) < 18 or int(result_age) > 46:  # 判断输入年龄
                    print '18 - 46岁才可以呦'
                    continue
                self.age = result_age
                break
            except Exception:
                print '你想早恋啊，再等几年吧'
                continue

    def viever_info(self):  # 定义查询角色信息方法
        print '''
        姓名:%s
        年龄:%s
        技能:%s
        工资:%s
        存款:%s
        爱情指数:%s
        预期存款:20万
        爱情指数:15
        ''' % (self.name, self.age, ' '.join(self.skill), self.salary, self.balance, self.love_heat)


class Personage:  # 定义角色类
        print '角色：1.屌丝男     2.白富美'

        def __init__(self):
            self.person_1 = Person()  # 人类的实例化
            self.person_2 = Person()  # 人类的实例化

        def choice_personage(self):  # 定义选择方法
            operation = {'1': self.person_1, '2': self.person_2}  # 操作字典
            while True:
                choice_input = raw_input('请选择角色:').strip()  # 输入选择的角色
                if len(choice_input) == 0:
                    continue    # 判断输入长度
                if operation.has_key(choice_input):   # 判断是否存在该键
                    if choice_input == '1':            # 判断输入是否为1
                        operation.get(choice_input).input_info()  # 取得方法
                        print '游戏初始化化'
                        for i in range(1, 20):  # 初始化打印
                            sys.stdout.write('*'+'->')
                            sys.stdout.flush()
                            time.sleep(0.5)
                        print
                        print '屌丝男的爱情故事正式开始！'
                        return operation.get(choice_input)
                        break
                    elif choice_input == '2':
                        print '此角色暂未开发！！'
                        continue
                else:
                    print '输入错误，请重新输入'


class Lover:  # 定义Lover 类
    def __init__(self, number=1):  # 定义构造方法
        self.number = number

    def make_proposal(self):  # 定义求婚方法
        if protagonist.balance >= 200000 and protagonist.love_heat >= 15:  # 判断存款和爱情热度
            print '女孩终于被你打动，同意了你的求婚，游戏结束'
            os.sys.exit()
        if protagonist.balance < 200000:
            print '存款不够，继续努力吧'

    def pursuit(self):  # 定义追求方法
        print '''
        1.烛光晚宴 (热度加1）单次消费500元
        2.看电影    (热度加2)单次消费200元
        3.买衣服 (热度加3)单次消费1000元
        4.旅游  (热度加4)单次消费10000元
        5.求婚
        6.返回
        '''
        oper_pursuit = {'1': [1, 500], '2': [2, 200], '3': [3, 1000], '4': [4, 10000], '5': self.make_proposal}  # 操作字典
        while True:
            choice_pursuit = raw_input('选择追求的方式:').strip()#输入追求方式
            if len(choice_pursuit) == 0:
                continue
            if oper_pursuit.has_key(choice_pursuit) and choice_pursuit != '5':  # 判断输入是否存在并且不能为5
                if protagonist.balance > oper_pursuit.get(choice_pursuit)[1]:  # 判断存款是否能够用来追求对象
                    protagonist.love_heat = protagonist.love_heat + oper_pursuit.get(choice_pursuit)[0]  # 热度计算
                    protagonist.balance = protagonist.balance - oper_pursuit.get(choice_pursuit)[1]  # 存款计算
                    print '爱情热度增加了%s，当前热度是%s,继续努力呦！' % (oper_pursuit.get(choice_pursuit)[0], protagonist.love_heat)
                    self.number += 1  # 追求标记
                    break
                else:
                    print '穷屌丝 赶紧挣钱去吧！'
            if choice_pursuit == '6':
                break
            elif choice_pursuit == '5':
                self.make_proposal()  # 调用求婚方法
                break
            else:
                print '哥 你输入错啦！'


class Story:  # 定义story类
    def __init__(self):
        pass

    def one(self):  # 定义第一个情节描述方法
        print '当年，他们第一次相遇，'
        time.sleep(1)
        print '他骑着自行车，她一个人背着书包慢慢的走着，'
        time.sleep(1)
        print '他经过她的身边，回头，然后相视而笑了。'
        time.sleep(1)
        print '这一幕永远地保留在了她的心底******再后来他们成为了恋人'
        for i in range(3):
            print '*****' + '####'*i + '%s年' % (i+1)
            time.sleep(1)

    def two(self):  # 定义第二个情节描述方法
        print '高考那年，他落榜了，而她考上了北京A大学'
        while True:
            choice = raw_input('我要去北京打工挣钱供她上学，是(Y),否(N):').strip()
            if len(choice) == 0:
                continue
            if choice == 'Y' or choice == 'y':
                break
            if choice == 'N' or choice == 'n':
                print '这么漂亮的姑娘难道你就不动心？，追求失败，游戏退出'
                os.sys.exit()
            else:
                continue

    def learn(self):  # 定义学习情节描述方法
        print '从此开始了几个月的学习之路：'
        for i in range(1, 15):
            sys.stdout.write('learning'+'->')
            sys.stdout.flush()
            time.sleep(0.5)
        print
        print '就这样你在某培训机构培训了几个月'

    def work(self):  # 定义工作情节描述方法
        print '你成功的面试上了一家公司当网管，每月工资大部分用来给她用来交学费'
        for i in range(1, 5):
            sys.stdout.write('*'*5+'@'*i+'%s年'%i)
            sys.stdout.flush()
            time.sleep(0.5)
        print
        print '4年后，她毕业了，找了一家高大上的公司，在公司里遇到了一位高富帅，两人比较暧昧，你有了危机感,你决定努力挽回。'

    def three(self):  # 定义第三个情节描述方法
        print '你的存款少，穷屌丝一个，她抛弃了你跟随了那个高富帅，你决定奋发图强！'

    def learn_python(self):
        print '后来你想不 在这样苦逼下去，去老男孩学了python'


class Strive(object):  # 定义奋斗类
    def __init__(self, number=1, targ=''):  # 定义构造函数
        self.number = number  # 标记
        self.targ = targ    # 标记

    def interview(self):   # 定义iterview面试方法

        interview_dic = {'1': ['linux', 5000], '2': ['linux', 'shell', 8000], '3': ['linux', 'python', 14000]}  # 操作字典
        while True:
            print"""
                1:公司A(要求linux)           工资:5000
                2:公司B(要求linux，shell)    工资:8000
                3:公司C(要求linux,python)    工资:14000
                4:返回
                """
            choice_interview = raw_input('选择你要面试的公司:').strip()   # 输入面试公司
            if len(choice_interview) == 0: continue                      # 判断输入长度
            if interview_dic.has_key(choice_interview):                  # 判断输入是否存在
                set_dic = set(interview_dic.get(choice_interview)[:-1])   # 将输入的值取出并集合化
                set_skill = set(protagonist.skill)
                if set_dic <= set_skill:                      # 判断2个集合从属关系
                    protagonist.salary = interview_dic.get(choice_interview)[-1]    # 计算工资
                    print '面试成功，当前公司，当前的工资是%s' % protagonist.salary
                    if self.number == 1:
                        obj_story.work()
                    self.number += 1
                    return True
                    break

                else:
                    lack_skill = ' '.join(list(set_dic-set_skill))  # 格式化集合
                    print '资格不够，没有%s技术经验' % lack_skill    # 格式化打印
                    break
            if choice_interview == '4':
                break

    def learn(self):  # 定义学习方法
        print '1.linux培训 4000 2.python 6000 '
        learn_dic = {'1': ['linux', 4000], '2': ['python', 6000]}  # 操作字典
        while True:
            choice_learn = raw_input('选择你想培训的语言 :').strip()  #输入要学习的语言
            if len(choice_learn) == 0:
                continue
            if learn_dic.has_key(choice_learn):   # 判断输入是否存在
                if protagonist.balance > learn_dic.get(choice_learn)[1]:          # 判断存款是否能够用来学习
                    protagonist.balance = protagonist.balance - learn_dic.get(choice_learn)[1]  # 存款计算
                    protagonist.skill.append(learn_dic.get(choice_learn)[0])  # 技能增加
                    print '你当前的存款为 %s' % protagonist.balance
                    self.targ = choice_learn
                    obj_story.learn()
                    return True
                    break
                else:
                    print '存款或热度不够，继续攒钱下次再来'
                    break
            else:
                print '输入错误请重新输入!'

    def save_money(self):  # 定义赚钱方法

        while True:
            work_time = raw_input('工作多长时间(月)?:').strip()  # 输入工作时间
            if len(work_time) == 0:
                continue    # 判断输入长度
            try:
                work_time = int(work_time)
                protagonist.balance = protagonist.balance + protagonist.salary * work_time   # 存款计算
                print '当前的存款是:%s' % protagonist.balance
                break
            except Exception :
                continue

    def work(self):   # 定义方法
        make_money = ''
        if self.number >= 2:
            make_money = '3.赚钱'
        print '1.面试  2.学习' + make_money + '4.返回' # 当面试一次之后 才能看到赚钱选项
        oper_work = {'1': self.interview, '2': self.learn}  # 操作字典
        if self.number >= 2:
            oper_work['3'] = self.save_money
        while True:
            choice_work = raw_input('选择努力方向:').strip()  # 输入努力方向
            if len(choice_work) == 0:
                continue
            if choice_work == '4':
                break
            if oper_work.has_key(choice_work):
                get_result = oper_work.get(choice_work)()
                print oper_work.get(choice_work)
                break
            else:
                print '输入错误'
                continue


obj_personage = Personage()  # Personage的实例化
protagonist = obj_personage.choice_personage()  # 返回选择的角色给主角
obj_lover = Lover()  # lover类实例化
obj_story = Story()  # story故事情节实例化
obj_story.one()   # 调用方法
obj_story.two()  # 调用方法
obj_strive = Strive()  # Strive类实例化


def strive_menu():   # 定义奋斗菜单函数
    obj_strive.work()  # 选择工作或学习
    if obj_strive.targ == '2':
        obj_story.learn_python()


def lover_menu():  # 定义lover_menu 函数
    obj_lover.pursuit()
    if obj_lover.number != 1:
        if protagonist.balance < 20000:
            obj_story.three()


def viever_menu():  # 查看当前用户信息
    protagonist.viever_info()


def game_exit():  # 退出系统
    print '退出系统'
    os.sys.exit()
menu_dic = {'1': strive_menu, '2': lover_menu, '3': viever_menu, '4': game_exit}
while True:
    print '1.努力奋斗 2.追求   3.查看角色属性， 4.退出'
    menu_input = raw_input('选择 :').strip()
    if len(menu_input) == 0:
        continue
    if menu_dic.has_key(menu_input):
        menu_dic.get(menu_input)()
    else:
        print '输入错误'









