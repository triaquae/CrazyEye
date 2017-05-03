from django.shortcuts import render,HttpResponse,HttpResponseRedirect,Http404,redirect

from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError

from django.contrib.auth.decorators import login_required

from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from  kingadmin_old.king_admin import site
from kingadmin_old import tables
from kingadmin_old import forms
from kingadmin_old.permissions import check_permission
import re,os ,datetime,random,string
from django.contrib.auth import login,logout,authenticate
from django.core.cache import cache


from kingadmin_old import settings



@check_permission
@login_required(login_url="/kingadmin_old/login/")
def app_index(request):

    return render(request,'kingadmin/app_index.html', {'enabled_admins':site.enabled_admins})

@login_required
def app_tables(request,app_name):

    enabled_admins = {app_name:site.enabled_admins[app_name]}


    return render(request, 'kingadmin/app_index.html',{'enabled_admins':enabled_admins,'current_app':app_name})


def acc_login(request):
    err_msg = {}
    today_str = datetime.date.today().strftime("%Y%m%d")
    # verify_code_img_path = "%s/%s" %(settings.VERIFICATION_CODE_IMGS_DIR,
    #                                  today_str)
    # if not os.path.isdir(verify_code_img_path):
    #     os.makedirs(verify_code_img_path,exist_ok=True)
    # #print("session:",request.session.session_key)
    # ##print("session:",request.META.items())
    #random_filename = "".join(random.sample(string.ascii_lowercase,4))
    # random_code = verify_code.gene_code(verify_code_img_path,random_filename)
    # cache.set(random_filename, random_code,30)

    if request.method == "POST":

        username = request.POST.get('username')
        password = request.POST.get('password')
        _verify_code = request.POST.get('verify_code')
        _verify_code_key  = request.POST.get('verify_code_key')

        ##print("verify_code_key:",_verify_code_key)
        ##print("verify_code:",_verify_code)
        if cache.get(_verify_code_key) == _verify_code:
            #print("code verification pass!")

            user = authenticate(username=username,password=password)
            if user is not None:
                login(request,user)
                request.session.set_expiry(60*60)
                return HttpResponseRedirect(request.GET.get("next") if request.GET.get("next") else "/kingadmin_old/")

            else:
                err_msg["error"] = 'Wrong username or password!'

        else:
            err_msg['error'] = "验证码错误!"

    #return render(request,'login.html',{"filename":random_filename, "today_str":today_str, "error":err_msg})
    return render(request,'kingadmin/login.html',{ "error":err_msg})





def acc_logout(request):

    logout(request)
    return HttpResponseRedirect("/kingadmin_old/login/")




@check_permission
@login_required(login_url="/kingadmin_old/login/")
def display_table_list(request,app_name,table_name):
    if app_name in site.enabled_admins:
        ##print(enabled_admins[url])
        if table_name in site.enabled_admins[app_name]:
            admin_class = site.enabled_admins[app_name][table_name]

            if request.method == "POST":  # action 来了

                ##print(request.POST)
                selected_ids = request.POST.get("selected_ids")
                action = request.POST.get("admin_action")
                if selected_ids:
                    selected_objs = admin_class.model.objects.filter(id__in=selected_ids.split(','))
                else:
                    raise KeyError("No object selected.")
                if hasattr(admin_class, action):
                    action_func = getattr(admin_class, action)
                    request._admin_action = action
                    return action_func(admin_class, request, selected_objs)



            if request.method == "POST2":
                #print('post-->', request.POST)

                delete_tag = request.POST.get("_delete_confirm")
                if delete_tag == "yes":
                    del_ids = request.POST.getlist("deleted_objs")

                    admin_class.model.objects.filter(id__in=del_ids).delete()

                else:

                    admin_action = request.POST.get('admin_action')
                    selected_raw_ids = request.POST.get('selected_ids','')
                    selected_ids = selected_raw_ids.split(',')
                    selected_objs = admin_class.model.objects.filter(id__in=selected_ids)

                    if hasattr(admin_class, admin_action):
                        admin_action_func = getattr(admin_class, admin_action)
                        return admin_action_func(admin_class,request,selected_objs)
                    else:
                        raise NotImplementedError("admin_action %s cannot find" % admin_action)


            querysets = tables.table_filter(request, admin_class,admin_class.model)
            searched_querysets = tables.search_by(request,querysets,admin_class)
            order_res = tables.get_orderby(request, searched_querysets, admin_class)

            paginator = Paginator(order_res[0], admin_class.list_per_page)

            page = request.GET.get('page')
            try:
                table_obj_list = paginator.page(page)
            except PageNotAnInteger:
                table_obj_list = paginator.page(1)
            except EmptyPage:
                table_obj_list = paginator.page(paginator.num_pages)

            table_obj = tables.TableHandler(request,
                                            admin_class.model,
                                            admin_class,
                                            table_obj_list,
                                            order_res)



            return render(request,'kingadmin/model_obj_list.html',
                                                    {'table_obj':table_obj,
                                                     'app_name':app_name,
                                                     'active_url': '/kingadmin_old/',
                                                     'paginator':paginator})

    else:
        raise Http404("url %s/%s not found" % (app_name,table_name) )



@check_permission
@login_required(login_url="/kingadmin_old/login/")
def table_change(request,app_name,table_name,obj_id):
    #print("table change:",app_name,table_name ,obj_id)

    if app_name in site.enabled_admins:
        if table_name in site.enabled_admins[app_name]:
            admin_class = site.enabled_admins[app_name][table_name]
            ##print(enabled_admins[table_name])
            obj = admin_class.model.objects.get(id=obj_id)
            ##print("obj....change",obj)
            fields = []
            for field_obj in admin_class.model._meta.fields:
                if field_obj.editable :
                    fields.append(field_obj.name)

            for field_obj in admin_class.model._meta.many_to_many:
                fields.append(field_obj.name)
            ##print('fields', fields)
            model_form = forms.create_form(admin_class.model, fields,admin_class,request=request)

            if request.method == "GET":
                form_obj = model_form(instance=obj)

            elif request.method == "POST":
                #print("post:",request.POST)
                form_obj = model_form(request.POST,instance=obj)
                if form_obj.is_valid():
                    form_obj.validate_unique()
                    if form_obj.is_valid():
                        form_obj.save()

            return render(request,'kingadmin/table_change.html',
                          {'form_obj':form_obj,
                           'active_url': '/kingadmin_old/',
                           'model_verbose_name':admin_class.model._meta.verbose_name,
                           'model_name':admin_class.model._meta.model_name,
                           'app_name':app_name,
                           'admin_class':admin_class

                            })
    else:
        raise Http404("url %s/%s not found" %(app_name,table_name)  )


@login_required(login_url="/kingadmin_old/login/")
def table_del(request,app_name,table_name,obj_id):

    if app_name in site.enabled_admins:
        if table_name in site.enabled_admins[app_name]:
            admin_class = site.enabled_admins[app_name][table_name]
            objs = admin_class.model.objects.filter(id=obj_id)
            if request.method == "POST":
                delete_tag = request.POST.get("_delete_confirm")
                if delete_tag == "yes":
                    objs.delete()
                    return redirect("/kingadmin_old/%s/%s/"%(app_name,table_name))

            if admin_class.readonly_table is True:
                return render(request, 'kingadmin/table_objs_delete.html')
            return render(request,'kingadmin/table_objs_delete.html',{
                'model_verbose_name': admin_class.model._meta.verbose_name,
                'model_name':admin_class.model._meta.model_name,
                'model_db_table':admin_class.model._meta.db_table,
                'objs':objs,
                'app_name':app_name,
                                    })


@login_required(login_url="/kingadmin_old/login/")
def table_add(request,app_name,table_name):
    #print("request :",request.POST)
    if app_name in site.enabled_admins:
        if table_name in site.enabled_admins[app_name]:
            fields = []
            admin_class = site.enabled_admins[app_name][table_name]
            for field_obj in admin_class.model._meta.fields:
                if field_obj.editable:
                    fields.append(field_obj.name)
            for field_obj in admin_class.model._meta.many_to_many:
                fields.append(field_obj.name)
            if admin_class.add_form == None:
                model_form = forms.create_form(admin_class.model,
                                               fields,
                                               admin_class,
                                               form_create=True,
                                               request=request)
            else: #this admin has customized  creation form defined
                model_form = admin_class.add_form

            if request.method == "GET":
                form_obj = model_form()
            elif request.method == "POST":
                form_obj = model_form(request.POST)
                if form_obj.is_valid():
                    form_obj.validate_unique()
                    if form_obj.is_valid():
                        form_obj.save()
                        if request.POST.get('_continue') is not None:

                            redirect_url = '%s/%s/' %( re.sub("add/$", "change",request.path), form_obj.instance.id)
                            #print('redirect url',redirect_url)
                            return redirect(redirect_url)
                        elif request.POST.get("_add_another") is not None:
                            #print('add another form', form_obj)
                            form_obj = model_form()

                        else: #return to table list page
                            redirect_url = request.path.rstrip("/add/")
                            return redirect(redirect_url)

            return render(request, 'kingadmin/table_add.html',
                          {'form_obj': form_obj,
                           'model_name': admin_class.model._meta.model_name,
                           'model_verbose_name': admin_class.model._meta.verbose_name,
                           'model_db_table':admin_class.model._meta.db_table,
                           'admin_class': admin_class,
                           'app_name': app_name,
                           'active_url': '/kingadmin_old/',
                           })

    else:
        raise Http404("url %s/%s not found" % (app_name,table_name))



@login_required(login_url="/kingadmin_old/login/")
def personal_password_reset(request):
    app_name = request.user._meta.app_label
    model_name  = request.user._meta.model_name


    if request.method == "GET":
        change_form = site.enabled_admins[app_name][model_name].add_form(instance=request.user)
    else:
        change_form = site.enabled_admins[app_name][model_name].add_form(request.POST, instance=request.user)
        if change_form.is_valid():
            change_form.save()
            url = "/%s/" % request.path.strip("/password/")
            return redirect(url)

    return render(request, 'kingadmin/password_change.html', {'user_obj': request.user,
                                                              'form': change_form})


@login_required(login_url="/kingadmin_old/login/")
def password_reset_form(request,app_name,table_db_name,user_id):
    user_obj = request.user._meta.model.objects.get(id=user_id)
    can_change_user_password = False
    if request.user.is_admin or request.user.id == user_obj.id :
        can_change_user_password = True

    if can_change_user_password:
        if request.method == "GET":
            change_form = site.enabled_admins[app_name][table_db_name].add_form(instance=user_obj)
        else:
            change_form = site.enabled_admins[app_name][table_db_name].add_form(request.POST,instance=user_obj)
            if change_form.is_valid():
                change_form.save()
                url = "/%s/" %request.path.strip("/password/")
                return redirect(url)

        return render(request,'kingadmin/password_change.html',{'user_obj':user_obj,
                                                      'form':change_form})

    else:
        return HttpResponse("Only admin user has permission to change password")