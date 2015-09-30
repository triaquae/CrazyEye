from django.shortcuts import render,HttpResponseRedirect,HttpResponse
from django.contrib import auth

from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
import host_mgr
# Create your views here.
import models,utils
import json
from CrazyEye import settings
import forms
from backend.utils import json_date_to_stamp,json_date_handler
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

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
    return render(request,'hosts.html',{'login_user':request.user,
                                         'selected_g_id': selected_g_id,
                                        'active_node':"/hosts/?selected_group=-1",
                                        'webssh':settings.WebSSH})

def login(request):
    #redirect_to_page = request.POST,request.GET.get('next')
    if request.method == "POST":

        username = request.POST.get('username')
        password = request.POST.get('password')
        user = auth.authenticate(username=username,password=password)
        if user is not None:
            auth.login(request,user)
            request.session.set_expiry(60*30)
            print 'session expires at :',request.session.get_expiry_date()
            return HttpResponseRedirect('/')
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
    #print 'log result:', task_result
    return HttpResponse(task_result)

@login_required
def file_download(request,task_id):

    print '=====>file download:',task_id
    #file_path = "%s/%s/%s" %(settings.BASE_DIR,settings.FileUploadDir,request.GET.get('task_id'))
    file_path = "%s/%s/%s/%s" %(settings.BASE_DIR,settings.FileUploadDir,request.user.userprofile.id,task_id)
    return utils.send_zipfile(request, task_id,file_path)

#below test
def article_detail(request,year,month,day,test):
    print '--->',year,month,day , test
    from django.http import Http404,HttpResponseNotFound
    return HttpResponseNotFound('<h1>Page not found</h1>')
    #raise  Http404("ttt")

@login_required
def token_gen(request):
    #token_type = request.POST.get('token_type')
    token = utils.Token(request)
    token_key = token.generate()

    return HttpResponse(token_key)


def dashboard_summary(request):

    if request.method == 'GET':


        summary_data = utils.dashboard_summary(request)
        return HttpResponse(json.dumps(summary_data,default=json_date_to_stamp))


def user_audit(request,user_id):

    user_obj = models.UserProfile.objects.get(id=int(user_id))
    department_list = models.Department.objects.all()
    user_login_records = models.AuditLog.objects.filter(user_id=user_obj.id,action_type=1).order_by('-date')
    user_multi_task_records = models.TaskLog.objects.filter(user_id= user_obj.id).order_by('-start_time')
    paginator = Paginator(user_login_records,10)
    paginator_multi = Paginator(user_multi_task_records,1)
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
        'active_node':'/user_audit/1',
        'data_type': data_type #for tab switch usage
    })



def multi_task_log_detail(request,task_id):

    log_obj = models.TaskLog.objects.get(id=task_id)

    return render(request,'multi_task_log_detail.html',{'log_obj':log_obj})

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



#---------below test ----------

def register(request):
    print 'SESSION:', dir(request.session)
    print request.session.session_key
    print request.session.get_expiry_age()
    print request.session.set_expiry(30)
    if request.method == 'GET':
        register_form = forms.RegistrationForm()
        return  render(request, 'register.html',{'form': register_form})
    else:
        print request.POST
        register_form = forms.RegistrationForm(request.POST)
        if register_form.is_valid():
            print '--->',register_form.cleaned_data
            return HttpResponse("register success!")
        else:
            print '---error:',register_form.errors
            return  render(request, 'register.html',{'form': register_form})

