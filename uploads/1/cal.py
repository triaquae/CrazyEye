#!/usr/bin/env python
#  _*_ coding:utf-8 _*_

import re

l1_pattern = re.compile(r'\([^()]*\)') # 匹配没有子级括号的算式
l2_pattern = re.compile(r'(-?\d+)(\.\d+)?[/*](-?\d+)(\.\d+)?')  # 匹配乘除法算式
l3_pattern = re.compile(r'(-?\d+)(\.\d+)?[-+](-?\d+)(\.\d+)?')  # 匹配加减法算式

mul_sub_pattern = re.compile(r'(-?\d+)(\.\d+)?\*-(-?\d+)(\.\d+)?')  # 匹配乘负数算式
div_sub_pattern = re.compile(r'(-?\d+)(\.\d+)?/-(-?\d+)(\.\d+)?')  # 匹配除负数算式


def min_cal(string): # 定义计算二元算式的函数
    if string.count('+') == 1:
        return str(float(string[:string.find('+')]) + float(string[string.find('+')+1:]))
    elif string[1:].count('-') == 1:
        return str(float(string[:string.find('-', 1)]) - float(string[string.find('-', 1)+1:]))
    elif string.count('*') == 1:
        return str(float(string[:string.find('*')]) * float(string[string.find('*')+1:]))
    elif string.count('/') == 1:
        return str(float(string[:string.find('/')]) / float(string[string.find('/')+1:]))

    '''
    此函数只用来处理二元算式字符串，即只有一个运算符的算式。返回值为此二元算式的最终结果字符串。
    计算方法为将运算符分割开的两部分字符串转换为float型数据并进行相应计算并返回重新格式化为字
    串的结果
    ***特殊情况***：当算式第一个数字为负数时，运算符为非首位的'-'字符
    '''


def nomal_numerator(string):  # 定义计算不带括号的算式计算函数
    if string.count('+') + string.count('*') + string.count('/') == 0 and string[1:].find('-') < 0:
        return string
    elif string.count('+-') + string.count('--') + string.count('*-') + string.count('/-') != 0:
        string = string.replace('+-', '-')
        string = string.replace('--', '+')
        if string.count('*-') != 0:
            string = string.replace(mul_sub_pattern.search(string).group(), '-'+mul_sub_pattern.search(string).group().replace('*-','*'))
        if string.count('/-') != 0:
            string = string.replace(div_sub_pattern.search(string).group(), '-'+div_sub_pattern.search(string).group().replace('/-','/'))
        return nomal_numerator(string)
    elif string.count('*') + string.count('/') != 0:
        from_str = l2_pattern.search(string).group()
        string = string.replace(from_str, min_cal(from_str))
        return nomal_numerator(string)
    elif string.count('+') != 0 or string.count('-') != 0:
        from_str = l3_pattern.search(string).group()
        string = string.replace(from_str, min_cal(from_str))
        return nomal_numerator(string)
    '''
    此函数采用递归的方法，仅用于处理不含括号的表达式，核心思想是如果表达式字符串中有乘法或除法运
    算符时，在每次调用时，将匹配到的二元乘法或除法算式用其结果字符串替代，结果通过min_cal()函数
    计算而来；如果没有乘除法运算符，则在每次调用时，将匹配道德二元加法或减法算式用其结果字符串替
    代，结果通过min_cal()函数计算而来；递归调用，直到字符串中不再有'+-*/'等字符（首位的'-'除外）
    ***特殊情况***：
    当二元算式字符串用结果替代的过程中，出现负数运算时，会出现运算符相连的情况，需要对其进行处理，
    一共有四中情况：
    '+-'：直接替换为'-'
    '--'：直接替换为'+'
    '*-' 或 '/-'：将'-'移到二元算式前面，如：'3*-5' --> '-3*5'
    '''


def l1_analysis(string):  # 定义括号式分解函数
    if string.find('(') == -1:
        return nomal_numerator(string)
    else:
        from_str = l1_pattern.search(string).group()
        string = string.replace(from_str, nomal_numerator(from_str[1:-1]))
        return l1_analysis(string)
    '''
    此函数采用递归的方法，仅用于将不含子级括号的算式用其括号内容表达式的结果替换，结果由normal_
    numerator()函数计算得出；递归调用，直到表达式最终解析为不含括号的普通表达式，由normal_nu
    merator()函数计算出最终结果
    '''


# test_data
# s = '1+2*3-(5-1)/2+(5+2)'
# s = '2*3/(5*1)*((5*2)/4)*4/3/2'
# s = '2+3-(5+1)-(5+2)'
# s = '32+(34-10/4)*(1+2-(3-5))'
# s = '2*3+(5*1)*((5*2)/4)-4'
# s = '(2*5+14/(2/2*5-2+10)+1)-131+3*(15-6*(10+5-2/5*5))-(18+3*(2+8-2/2*5)-21/10)+110'

while True:
    s = raw_input("请输入算式(输入exit以退出)： \n")
    s = s.replace(' ', '')
    if s == 'exit':
        break
    else:
        print "结果为： \n", l1_analysis(s)


