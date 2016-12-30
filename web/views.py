#_*_coding:utf-8_*_
from django.shortcuts import render,HttpResponseRedirect,HttpResponse,redirect
from django.http import HttpResponseNotFound,Http404
from django.contrib import auth

from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from web import host_mgr
# Create your views here.
from web import models,utils
import json,datetime,os,time
from CrazyEye import settings
from  web import forms
from backend.utils import json_date_to_stamp,json_date_handler
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import django.utils.timezone
from django.core.exceptions import ObjectDoesNotExist
from web import tables
from web import admin
from web.king_admin import enabled_admins
from backend import audit as session_audit
from web import permissions
import random,string


@permissions.check_permission
@login_required
def dashboard(request):
    if request.user.is_superuser:
        recent_tasks= models.TaskLog.objects.all().order_by('-id')[:10]
        return render(request,'index.html',{
            'login_user':request.user,
            'recent_tasks':recent_tasks
        })
    else:
        return  HttpResponseRedirect('/hosts/')


@login_required
def hosts(request):

    selected_g_id = request.GET.get('selected_group')
    if selected_g_id:
        if selected_g_id.isdigit():
            selected_g_id = int(selected_g_id)

    recent_logins = utils.recent_accssed_hosts(request)

    return render(request,'hosts.html',{'login_user':request.user,
                                         'selected_g_id': selected_g_id,
                                        'active_node':"/hosts/?selected_group=-1",
                                        'recent_logins':recent_logins,
                                        'webssh':settings.SHELLINABOX})

def login(request):

    if request.method == "POST":

        username = request.POST.get('username')
        password = request.POST.get('password')
        user = auth.authenticate(username=username,password=password)
        if user is not None:
            try:
                if user.valid_begin_time and user.valid_end_time:
                    if django.utils.timezone.now() > user.valid_begin_time and django.utils.timezone.now()  < user.valid_end_time:
                        auth.login(request,user)
                        request.session.set_expiry(60*30)
                        return HttpResponseRedirect(request.GET.get("next") if request.GET.get("next") else "/")
                    else:
                        return render(request,'login.html',{'login_err': 'User account is expired,please contact your IT guy for this!'})
                else:
                    auth.login(request, user)
                    request.session.set_expiry(60 * 30)
                    return HttpResponseRedirect(request.GET.get("next") if request.GET.get("next") else "/")

            except ObjectDoesNotExist:
                    return render(request,'login.html',{'login_err': u'CrazyEye账户还未设定,请先登录后台管理界面创建CrazyEye账户!'})

        else:
            return render(request,'login.html',{'login_err': 'Wrong username or password!'})
    else:
        return render(request, 'login.html')

@login_required
def personal(request):
    if request.method == 'POST':
        msg = {}
        old_passwd = request.POST.get('old_passwd')

        new_password = request.POST.get('new_passwd')
        user = auth.authenticate(username=request.user.email,password=old_passwd)
        if user is not None:
            request.user.set_password(new_password)
            request.user.save()
            msg['msg'] = 'Password has been changed!'
            msg['res'] = 'success'
        else:
            msg['msg'] = 'Old password is incorrect!'
            msg['res'] = 'failed'

        return HttpResponse(json.dumps(msg))
    else:
        return render(request,'personal.html',{'info_form':forms.UserProfileForm()})

@login_required
def logout(request):
    auth.logout(request)
    return HttpResponseRedirect("/")



@login_required
def password_reset_form(request,table_db_name,user_id):
    user_obj = models.UserProfile.objects.get(id=user_id)
    if request.method == "GET":
        change_form = enabled_admins[table_db_name].add_form(instance=user_obj)
    else:
        change_form = enabled_admins[table_db_name].add_form(request.POST,instance=user_obj)
        if change_form.is_valid():
            change_form.save()
            url = "/%s/" %request.path.strip("/password/")
            return redirect(url)

    return render(request,'password_change.html',{'user_obj':user_obj,
                                                  'form':change_form})


@permissions.check_permission
@login_required
def hosts_multi(request):
    #valid_hosts = host_mgr.valid_host_list(request) #dict
    recent_tasks = models.TaskLog.objects.filter(user_id=1).order_by('-id')[:10]


    return render(request,'hosts_multi.html',{'login_user':request.user,
                                              #'host_groups':valid_hosts,
                                              'recent_tasks': recent_tasks,
                                              'active_node':'/hosts/multi'})

@login_required
def multitask_cmd(request):
    #print '==post:',request.POST
    multi_task = host_mgr.MultiTask('run_cmd',request)
    task_id = multi_task.run()
    if task_id:
        return HttpResponse(task_id)
    else:
        return HttpResponse("TaskCreatingError")

@login_required
def crontab(request):
    return  render(request,'crontab.html',{'active_node':'/hosts/crontab/'})


@permissions.check_permission
@login_required
def hosts_multi_filetrans(request):

    random_str = ''.join(random.sample(string.ascii_lowercase,8))
    recent_tasks = models.TaskLog.objects.filter(user_id=1).order_by('-id')[:10]


    return render(request,'hosts_multi_files.html',{'login_user':request.user,
                                              'recent_tasks': recent_tasks,
                                              'random_str': random_str,
                                              'active_node':'/hosts/multi/filetrans'})



def get_uploaded_fileinfo(file_dic,upload_dir):
    for filename in os.listdir(upload_dir):
        abs_file = '%s/%s' % (upload_dir, filename)
        file_create_time = time.strftime("%Y-%m-%d %H:%M:%S",
                                         time.gmtime(os.path.getctime(abs_file)))
        file_dic['files'][filename] = {'size': os.path.getsize(abs_file) / 1000,
                                           'ctime': file_create_time}


@login_required
@csrf_exempt
def multitask_file_upload(request,random_str):
    print('---random str:',random_str,request.FILES)
    upload_dir = "%s/task_data/tmp/%s" %(settings.FileUploadDir,random_str)
    response_dic = {'files':{}}
    utils.handle_upload_file(request,random_str,response_dic)
    get_uploaded_fileinfo(response_dic, upload_dir)

    return HttpResponse(json.dumps(response_dic))
@login_required
def multitask_file(request):
    multi_task = host_mgr.MultiTask(request.POST.get('task_type'),request)
    task_result = multi_task.run()
    return  HttpResponse(task_result)




@login_required
def delete_file(request,random_str):
    response = {}
    if request.method == "POST":
        upload_dir = "%s/task_data/tmp/%s" % (settings.FileUploadDir,random_str)
        filename = request.POST.get('filename')
        file_abs = "%s/%s" %(upload_dir,filename.strip())
        if os.path.isfile(file_abs):
            os.remove(file_abs)
            response['msg'] = "file '%s' got deleted " % filename
        else:
            response["error"] = "file '%s' does not exist on server"% filename
    else:
        response['error'] = "only supoort POST method..."
    return HttpResponse(json.dumps(response))


@login_required
def multitask_res(request):
    multi_task = host_mgr.MultiTask('get_task_result',request)
    task_result = multi_task.run()
    return HttpResponse(task_result)

@login_required
def file_download(request,task_id):

    file_path = "%s/task_data/%s" %(settings.FileUploadDir,task_id)
    return utils.send_zipfile(request, task_id,file_path)


@login_required
def token_gen(request):
    #token_type = request.POST.get('token_type')
    token = utils.Token(request)
    token_key = token.generate()

    return HttpResponse(token_key)

@login_required
def dashboard_summary(request):

    if request.method == 'GET':


        summary_data = utils.dashboard_summary(request)
        return HttpResponse(json.dumps(summary_data,default=json_date_to_stamp))

@login_required
def dashboard_detail(request):
    if request.method == 'GET':
        detail_ins = utils.Dashboard(request)
        res = list(detail_ins.get())
        return HttpResponse(json.dumps(res,default=json_date_handler))

@login_required
def host_detail(request):
    host_id = request.GET.get('host_id')
    access_records = []

    all_hosts = models.Hosts.objects.all()
    if host_id:
        host_id = int(host_id)

        #access_records = models.AuditLog.objects.filter(host__host_id=host_id,action_type=1).order_by('-date')
        access_records = models.Session.objects.filter(bind_host__host_id=host_id).order_by('-date')
        #print("acc records;",access_records)

        paginator = Paginator(access_records,10)
        page = request.GET.get('page')
        try:
            access_records = paginator.page(page)
        except PageNotAnInteger:
            access_records = paginator.page(1)
        except EmptyPage:
            access_records = paginator.page(paginator.num_pages)


    return  render(request, 'host_detail.html', {'all_hosts':all_hosts,
                                                 'current_host_id': host_id,
                                                 'access_records': access_records,
                                                 'active_node':'/host/detail/'})


@login_required
def user_audit(request,user_id):

    user_obj = models.UserProfile.objects.get(id=int(user_id))
    department_list = models.Department.objects.all()
    user_login_records = models.AuditLog.objects.filter(user_id=user_obj.id,action_type=1).order_by('-date')
    user_multi_task_records = models.TaskLog.objects.filter(user_id= user_obj.id).order_by('-start_time')
    paginator = Paginator(user_login_records,10)
    paginator_multi = Paginator(user_multi_task_records,10)
    page = request.GET.get('page')
    data_type = request.GET.get('type')

    try:
        login_records = paginator.page(page)
    except PageNotAnInteger:
        login_records = paginator.page(1)
    except EmptyPage:
        login_records = paginator.page(paginator.num_pages)

    try:
        multitask_records = paginator_multi.page(page)
    except PageNotAnInteger:
        multitask_records = paginator_multi.page(1)
    except EmptyPage:
        multitask_records = paginator_multi.page(paginator_multi.num_pages)


    return  render(request,'user_audit.html',{
        'department_list':department_list,
        'user_obj':user_obj,
        'user_login_records':login_records,
        'multitask_records':multitask_records,
        'active_node':'/user_audit/1/',
        'data_type': data_type #for tab switch usage
    })


@login_required
def audit(request):

    audit_log_list = tables.table_filter(request,admin.AuditLogAdmin,models.AuditLog)
    order_res = tables.get_orderby(request, audit_log_list, admin.AuditLogAdmin)
    paginator = Paginator(order_res[0], admin.AuditLogAdmin.list_per_page)

    page = request.GET.get('page')
    try:
        audit_log_objs = paginator.page(page)
    except PageNotAnInteger:
        audit_log_objs = paginator.page(1)
    except EmptyPage:
        audit_log_objs = paginator.page(paginator.num_pages)

    table_obj = tables.TableHandler(request,
                                    models.AuditLog,
                                    admin.AuditLogAdmin,
                                    audit_log_objs,
                                    order_res)

    return render(request,"audit.html",{'table_obj':table_obj,
                                        'paginator':paginator})




@login_required
def multitask_task_action(request):
    if request.method == 'POST':
        action = request.POST.get('action')
        m = host_mgr.MultiTask(action,request)
        res = m.run()

        return  HttpResponse(json.dumps(res))

@login_required
def multi_task_log_detail(request,task_id):

    log_obj = models.TaskLog.objects.get(id=task_id)

    return render(request,'multi_task_log_detail.html',{'log_obj':log_obj})

@login_required
def audit_cmd_logs(request):
    session_id  = request.GET.get('session_id')
    if session_id:
        session_id = int(session_id)
        cmd_records = list(models.AuditLog.objects.filter(session_id = session_id).values().order_by('date'))

        data = {
            'data':cmd_records,
            'action_choices':models.AuditLog.action_choices
        }

        return  HttpResponse(json.dumps(data,default=json_date_handler))

@login_required
def user_login_counts(request):
    filter_time_stamp = request.GET.get('time_stamp')
    assert  filter_time_stamp.isdigit()
    filter_time_stamp = int(filter_time_stamp) / 1000
    filter_date_begin = datetime.datetime.fromtimestamp(filter_time_stamp)
    filter_date_end = filter_date_begin + datetime.timedelta(days=1)

    user_login_records = models.Session.objects.filter(date__range=[filter_date_begin,filter_date_end]).\
        values('bind_host',
               'bind_host__host_user__username',
               'user',
               'user__name',
               'bind_host__host__hostname',
               'date')

    return  HttpResponse(json.dumps(list(user_login_records),default=json_date_handler))



@login_required
def session_reccord(request,session_id):
    try:

        session_obj = models.Session.objects.get(id=session_id)
        print("session obj:",session_obj)
        session_log_file = "%s/%s/session_%s.log" %(settings.SESSION_AUDIT_LOG_DIR,
                                                    session_obj.date.strftime( "%Y_%m_%d"),
                                                    session_obj.id)

        if os.path.isfile(session_log_file):
            log_wash = session_audit.AuditLogHandler(session_log_file)
            log_data = log_wash.parse()
            #update session stay time and cmd count
            session_obj.cmd_count = len(log_data)
            if len(log_data ) >1:
                last_cmd_time = log_data[-1][0]
                last_cmd_datetime_str = "%s %s"%(session_obj.date.strftime( "%Y_%m_%d"), last_cmd_time)
                #print("last_cmd_datetime_str",last_cmd_datetime_str)
                last_cmd_struct_time = time.strptime(last_cmd_datetime_str,"%Y_%m_%d %H:%M:%S")
                last_cmd_timestamp = time.mktime(last_cmd_struct_time)
                #print('last cmd timestamp:',last_cmd_timestamp)
                session_obj.stay_time = last_cmd_timestamp - session_obj.date.timestamp()
                session_obj.save()
        else:
            log_data = [['n/a','---no session log---']]
        # if os.path.isfile(session_log_file):
        #     session_log = open(session_log_file).read()
        # else:
        #     print('file not exist ',session_log_file)
        #     session_log = '---no session log---'

        return render(request,"session_log.html",{'session_data':log_data,'session_obj':session_obj})
    except ObjectDoesNotExist as e:
        return HttpResponse(e)


@permissions.check_permission
@login_required
def configure_url_dispatch(request,url):
    print('---url dispatch',url)
    #print(enabled_admins)
    if url in enabled_admins:
        #print(enabled_admins[url])

        if request.method == "POST":
            print('post-->', request.POST)

            delete_tag = request.POST.get("_delete_confirm")
            if delete_tag == "yes":
                del_ids = request.POST.getlist("deleted_objs")

                enabled_admins[url].model.objects.filter(id__in=del_ids).delete()

            else:

                admin_action = request.POST.get('admin_action')

                admin_obj = enabled_admins[url]
                if hasattr(admin_obj, admin_action):
                    admin_action_func = getattr(admin_obj, admin_action)
                    return admin_action_func(request)
                else:
                    raise NotImplementedError("admin_action %s cannot find" % admin_action)


        querysets = tables.table_filter(request, enabled_admins[url],
                                        enabled_admins[url].model)
        searched_querysets = tables.search_by(request,querysets,enabled_admins[url])
        order_res = tables.get_orderby(request, searched_querysets, enabled_admins[url])

        paginator = Paginator(order_res[0], enabled_admins[url].list_per_page)

        page = request.GET.get('page')
        try:
            table_obj_list = paginator.page(page)
        except PageNotAnInteger:
            table_obj_list = paginator.page(1)
        except EmptyPage:
            table_obj_list = paginator.page(paginator.num_pages)

        table_obj = tables.TableHandler(request,
                                        enabled_admins[url].model,
                                        enabled_admins[url],
                                        table_obj_list,
                                        order_res)



        return render(request,'king_admin/model_obj_list.html',
                                                {'table_obj':table_obj,
                                                 'active_node': '/configure/index/',
                                                 'paginator':paginator})

    else:
        raise Http404("url %s not found" % url )

@permissions.check_permission
@login_required
def table_change(request,table_name,obj_id):
    print("table change:",table_name ,obj_id)
    if table_name in enabled_admins:
        #print(enabled_admins[table_name])
        obj = enabled_admins[table_name].model.objects.get(id=obj_id)
        #print("obj....change",obj)
        fields = []
        for field_obj in enabled_admins[table_name].model._meta.fields:
            if field_obj.editable :
                fields.append(field_obj.name)

        for field_obj in enabled_admins[table_name].model._meta.many_to_many:
            fields.append(field_obj.name)
        #print('fields', fields)
        model_form = forms.create_form(enabled_admins[table_name].model, fields,enabled_admins[table_name])

        if request.method == "GET":
            form_obj = model_form(instance=obj)

        elif request.method == "POST":
            print("post:",request.POST)
            form_obj = model_form(request.POST,instance=obj)
            if form_obj.is_valid():
                form_obj.save()

        return render(request,'king_admin/table_change.html',
                      {'form_obj':form_obj,
                      'active_node': '/configure/index/',
                      'model_name':enabled_admins[table_name].model._meta.verbose_name,
                      'model_db_table': enabled_admins[table_name].model._meta.db_table,
                       'admin_class':enabled_admins[table_name]

                        })
    else:
        raise Http404("url %s not found" % table_name )


@permissions.check_permission
@login_required
def configure_index(request):

    return render(request,'king_admin/index.html', {'enabled_admins':enabled_admins})

def table_add(request,table_name):
    print("request path:",request.path)
    if table_name in enabled_admins:
        fields = []
        for field_obj in enabled_admins[table_name].model._meta.fields:
            if field_obj.editable:
                fields.append(field_obj.name)
        for field_obj in enabled_admins[table_name].model._meta.many_to_many:
            fields.append(field_obj.name)
        if enabled_admins[table_name].add_form == None:
            model_form = forms.create_form(enabled_admins[table_name].model, fields,enabled_admins[table_name],form_create=True)
        else: #this admin has customized  creation form defined
            model_form = enabled_admins[table_name].add_form

        if request.method == "GET":
            form_obj = model_form()
        elif request.method == "POST":
            print(request.POST)
            form_obj = model_form(request.POST)
            if form_obj.is_valid():
                form_obj.save()
                print("form obj:",form_obj.cleaned_data,form_obj.instance.id)
                redirect_url = '/%s/change/%s' %(request.path.strip("/add"), form_obj.instance.id)
                if request.POST.get('_continue') is  None:#save and add another button
                    return redirect(redirect_url)

                #print("----continue....",request.POST)
                form_obj = model_form()

        return render(request, 'king_admin/table_add.html',
                      {'form_obj': form_obj,
                       'active_node': '/configure/index/',
                       'model_name': enabled_admins[table_name].model._meta.verbose_name,
                       'model_db_table':enabled_admins[table_name].model._meta.db_table,
                       'admin_class': enabled_admins[table_name]
                       })

    else:
        raise Http404("url %s not found" % table_name)


def table_del(request,table_name,obj_id):

    if table_name in enabled_admins:
        obj = enabled_admins[table_name].model.objects.get(id=obj_id)

        return render(request,'king_admin/table_delete.html',{
            'model_name': enabled_admins[table_name].model._meta.verbose_name,
            'model_table_name':enabled_admins[table_name].model._meta.model_name,
            'model_db_table':enabled_admins[table_name].model._meta.db_table,
            'obj':obj,
            'app_label':obj._meta.app_label
                                })