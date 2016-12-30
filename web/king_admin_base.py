
from django.http import HttpResponse
from django.shortcuts import render

class ModelAdminBase(object):
    add_form = None
    list_display = ()
    list_per_page = 20
    choice_fields = ()
    fk_fields = ()
    filter_horizontal = ()
    model = None
    onclick_fields = {}
    change_page_onclick_fields = {}

    readable_table = False
    search_fields = []
    readonly_fields = []

    default_actions = ['delete_selected','ddd']


    def delete_selected(self,request):
        print('delete  selected----',self,request)
        selected_ids = request.POST.get("selected_ids")
        if selected_ids:
            selected_ids = selected_ids.split(',')
        else:
            raise ValueError("no object got selected")

        objs = self.model.objects.filter(id__in=selected_ids)


        return render(request,'king_admin/table_objs_delete.html',{'objs':objs})

    delete_selected.short_description = "删除选中的数据"



def register(admin_dic,admin_class):
    '''注册admin'''
    if admin_class.model._meta.db_table not in admin_dic:
        admin_dic[admin_class.model._meta.db_table] = admin_class()
    else:
        raise Exception

