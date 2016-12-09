#_*_coding:utf-8_*_



from django.core.urlresolvers import resolve
from django.shortcuts import render,redirect,HttpResponse
from web.permission_list import perm_dic
from CrazyEye import settings


def perm_check(*args,**kwargs):

    request = args[0]
    resolve_url_obj = resolve(request.path)
    curr_url_name = resolve_url_obj.url_name  # 当前url的url_name
    print('---perm:',request.user,request.user.is_authenticated(),resolve_url_obj)
    match_flag = False
    match_key = None
    if request.user.is_authenticated() is False:
         return redirect(settings.LOGIN_URL)

    for per_key,per_val in  perm_dic.items():
        per_url_name, per_meth,per_arg = per_val
        if per_url_name == curr_url_name: #matched current request url
            if per_meth == request.method: #matched request method
                if not  per_arg: #if no args defined in perm dic, then set this request to passed perm check
                    match_flag = True
                    match_key = per_key
                else:

                    #逐个匹配参数，看每个参数时候都能对应的上。
                    for item in per_arg:
                        request_method_fun = getattr(request,request.per_meth)
                        if request_method_fun.get(item,None):# request字典中由此参数
                            match_flag = True
                        else:
                            match_flag = False
                            break  # 有一个参数不能匹配成功，则判定为假，退出该循环。

                    if match_flag == True:
                        match_key = per_key
                        break



    if match_flag:
        app_name, *per_name = match_key.split('_')
        print("--->matched ",match_flag,match_key)
        print(app_name, *per_name)
        perm_obj = '%s.%s' % (app_name,match_key)
        print("perm str:",perm_obj)
        if request.user.has_perm(perm_obj):
            print('当前用户有此权限')
            return True
        else:
            print('当前用户没有该权限')
            return False







def check_permission(func):
    def inner(*args,**kwargs):
        if not perm_check(*args,**kwargs):
            request = args[0]
            return render(request,'page_403.html')
        return func(*args,**kwargs)
    return  inner


