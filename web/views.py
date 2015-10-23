#_*_coding:utf-8_*_
from django.shortcuts import render,HttpResponseRedirect,HttpResponse
from django.contrib import auth

from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
import host_mgr
# Create your views here.
import models,utils
import json,datetime
from CrazyEye import settings
import forms
from backend.utils import json_date_to_stamp,json_date_handler
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import django.utils.timezone
from django.core.exceptions import ObjectDoesNotExist

@login_required
def dashboard(request):
    if request.user.is_superuser:
        recent_tasks= models.TaskLog.objects.all()[:10]
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
                if django.utils.timezone.now() > user.userprofile.valid_begin_time and django.utils.timezone.now()  < user.userprofile.valid_end_time:
                    auth.login(request,user)
                    request.session.set_expiry(60*30)
                    #print 'session expires at :',request.session.get_expiry_date()
                    return HttpResponseRedirect('/')
                else:
                    return render(request,'login.html',{'login_err': 'User account is expired,please contact your IT guy for this!'})
            except ObjectDoesNotExist:
                    return render(request,'login.html',{'login_err': u'CrazyEye账户还未设定,请先登录后台管理界面创建CrazyEye账户!'})

        else:
            return render(request,'login.html',{'login_err': 'Wrong username or password!'})
    else:
        return render(request, 'login.html')

@login_required
def personal(request):
    if request.method == 'POST':
        print request.POST
        msg = {}
        old_passwd = request.POST.get('old_passwd')

        new_password = request.POST.get('new_passwd')
        user = auth.authenticate(username=request.user.username,password=old_passwd)
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

@login_required
def hosts_multi_filetrans(request):
    recent_tasks = models.TaskLog.objects.filter(user_id=1).order_by('-id')[:10]


    return render(request,'hosts_multi_files.html',{'login_user':request.user,
                                              'recent_tasks': recent_tasks,
                                              'active_node':'/hosts/multi/filetrans'})

@login_required
@csrf_exempt
def multitask_file_upload(request):
    filename = request.FILES['filename']
    print '-->',request.POST
    utils.handle_upload_file(request,filename)

    return HttpResponse(json.dumps({'text':'success'}))
@login_required
def multitask_file(request):
    print 'multitask_file:',request.POST
    multi_task = host_mgr.MultiTask(request.POST.get('task_type'),request)
    task_result = multi_task.run()
    return  HttpResponse(task_result)

@login_required
def multitask_res(request):
    multi_task = host_mgr.MultiTask('get_task_result',request)
    task_result = multi_task.run()
    return HttpResponse(task_result)

@login_required
def file_download(request,task_id):

    file_path = "%s/%s/%s/%s" %(settings.BASE_DIR,settings.FileUploadDir,request.user.userprofile.id,task_id)
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
        print '-->',res
        return HttpResponse(json.dumps(res,default=json_date_handler))

@login_required
def host_detail(request):
    host_id = request.GET.get('host_id')
    access_records = []

    all_hosts = models.Hosts.objects.all()
    if host_id:
        host_id = int(host_id)

        access_records = models.AuditLog.objects.filter(host__host_id=host_id,action_type=1).order_by('-date')
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
def multitask_task_action(request):
    if request.method == 'POST':
        action = request.POST.get('action')
        m = host_mgr.MultiTask(action,request)
        res = m.run()
        print '-->task res:',res

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

    user_login_records = models.AuditLog.objects.filter(action_type=1,date__range=[filter_date_begin,filter_date_end]).values('host','host__host_user__username','user','user__name','host__host__hostname','session','date')

    print user_login_records
    return  HttpResponse(json.dumps(list(user_login_records),default=json_date_handler))

