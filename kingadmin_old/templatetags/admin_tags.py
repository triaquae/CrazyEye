#_*_coding:utf-8_*_
__author__ = 'jieli'
import datetime
import re
from django import template


from django.utils.safestring import mark_safe,mark_for_escaping
from  django.core.urlresolvers import reverse as url_reverse

register = template.Library()



@register.simple_tag
def query_set(table_related_field,query_field,string):

    data_set = table_related_field.filter(**{query_field:string}).count()

    return data_set

@register.simple_tag
def query_logout_date(obj, query_field, string):
    data_set = obj.filter(**{query_field:string})
    if data_set:

        return data_set[0].date.strftime("%Y-%m-%d %H:%M:%S")


@register.simple_tag
def get_table_column(column, table_obj):
    if hasattr(table_obj.model_class,column):
        return  table_obj.model_class._meta.get_field(column).verbose_name
    else:#might be customized field,which is not exist in model class
        #check if this field exist in admin class
        if hasattr(table_obj.admin_class, column):
            field_func = getattr(table_obj.admin_class,column)
            if hasattr(field_func,'display_name'):
                return field_func.display_name
            return field_func.__name__

@register.simple_tag
def load_search_element(table_obj):
    #print("search:",table_obj.search_fields)
    if table_obj.search_fields:
        already_exist_ars = ''
        for k,v in table_obj.request.GET.items():
            if k != 'q':#igonore old search text
                already_exist_ars += "<input type='hidden' name='%s' value='%s' >" % (k,v)
        placeholder = "search by %s" % ",".join(table_obj.search_fields)
        ele = '''
            <div class="searchbox">
               <form method="get">
                    <div class="input-group custom-search-form">
                        <input type="text" name="q" value='%s' class="form-control" placeholder="%s">
                        %s
                        <span class="input-group-btn">
                            <button class="text-muted" type="button"><i class="fa fa-search"></i></button>
                        </span>
                    </div>
               </form>
           </div>

        '''% (table_obj.request.GET.get('q') if table_obj.request.GET.get('q') else '',
              placeholder,already_exist_ars)
        return mark_safe(ele)
    return ''


@register.simple_tag
def display_orderby_arrow(table_obj,loop_counter):
    if table_obj.orderby_col_index == loop_counter:
        if table_obj.orderby_field.startswith('-'):#降序
            orderby_icon = '''<i class="fa fa-caret-up" aria-hidden="true"></i>'''
        else:
            orderby_icon = '''<i class="fa fa-caret-down" aria-hidden="true"></i>'''
        return mark_safe(orderby_icon)
    return ''



@register.simple_tag
def build_table_row(row_obj,table_obj,onclick_column=None,target_link=None):
    row_ele = "<tr>"

    row_ele += "<td><input type='checkbox' tag='row-check' value='%s' > </td>" % row_obj.id
    if table_obj.list_display:
        for index,column_name in enumerate(table_obj.list_display):

            if hasattr(row_obj,column_name):
                field_obj = row_obj._meta.get_field(column_name)
                column_data = field_obj._get_val_from_obj(row_obj)
                if field_obj.choices:#choices type
                    column_data = getattr(row_obj,"get_%s_display" % column_name)()
                else:
                    column_data = getattr(row_obj,column_name)

                #if column_name in table_obj.fk_fields:
                #    column_data = r"%s" %getattr(row_obj,column_name).__str__().strip("<>")
                if 'DateTimeField' in field_obj.__repr__():
                    column_data = getattr(row_obj,column_name).strftime( "%Y-%m-%d %H:%M:%S") \
                            if getattr(row_obj,column_name) else None
                if 'ManyToManyField' in field_obj.__repr__():
                    column_data = getattr(row_obj, column_name).select_related().count()
                if onclick_column == column_name:
                    column = ''' <td><a class='btn-link' href=%s>%s</a></td> '''% (url_reverse(target_link,args=(column_data, )),column_data)
                #if column_name in table_obj.onclick_fields:
                #    column = '''<td><a class='btn-link' href='%s' target='_blank'>%s</a></td>''' % \
                #             (url_reverse(table_obj.onclick_fields[column_name],args=(row_obj.id, )), column_data)

                elif index == 0:#首列可点击进入更改页
                    column = '''<td><a class='btn-link'  href='%schange/%s/' >%s</a> </td> ''' %(table_obj.request.path,
                                                                               row_obj.id,
                                                                               column_data)
                elif column_name in table_obj.colored_fields: #特定字段需要显示color
                    color_dic = table_obj.colored_fields[column_name]
                    if column_data in color_dic:
                        column = "<td style='background-color:%s'>%s</td>" % (color_dic[column_data],
                                                                   column_data)
                    else:
                        column = "<td>%s</td>" % column_data
                else:
                    column = "<td>%s</td>" % column_data

            elif hasattr(table_obj.admin_class, column_name): #customized field
                field_func = getattr(table_obj.admin_class, column_name)
                table_obj.admin_class.instance = row_obj
                column = "<td>%s</td>" % field_func(table_obj.admin_class)

            row_ele += column
    else:
        row_ele += "<td><a class='btn-link'  href='{request_path}change/{obj_id}/' >{column}</a></td>".\
            format(request_path=table_obj.request.path,column=row_obj, obj_id=row_obj.id)



    #for dynamic display
    if table_obj.dynamic_fk :
        if hasattr(row_obj,table_obj.dynamic_fk ):
            ##print("----dynamic:",getattr(row_obj,table_obj.dynamic_fk), row_obj)
            ##print(row_obj.networkdevice)
            dy_fk = getattr(row_obj,table_obj.dynamic_fk) #拿到的是asset_type的值
            if hasattr(row_obj,dy_fk):
                dy_fk_obj = getattr(row_obj,dy_fk)
                #print("-->type",type(dy_fk_obj), dy_fk_obj )
                for index,column_name in enumerate(table_obj.dynamic_list_display):
                    if column_name in table_obj.dynamic_choice_fields:
                        column_data = getattr(dy_fk_obj, 'get_%s_display' % column_name)()
                    else:
                        column_data = dy_fk_obj._meta.get_field(column_name)._get_val_from_obj(dy_fk_obj)
                    #print("dynamic column data", column_data)

                    column = "<td>%s</td>" % column_data
                    row_ele += column
            else:
                #这个关联的表还没创建呢
                pass
    row_ele += "</tr>"
    return mark_safe(row_ele)


@register.simple_tag
def render_page_num(request,paginator_obj,loop_counter):
    abs_full_url = request.get_full_path()

    if "?page=" in abs_full_url:
        url = re.sub("page=\d+", "page=%s" % loop_counter, request.get_full_path())
    elif "?" in abs_full_url:
        url = "%s&page=%s" % (request.get_full_path(), loop_counter)
    else:
        url = "%s?page=%s" % (request.get_full_path(), loop_counter)


    if loop_counter == paginator_obj.number: #current page
        return mark_safe('''<li class='active'><a href="{abs_url}">{page_num}</a></li>'''\
            .format(abs_url=url,page_num=loop_counter))


    if abs(loop_counter - paginator_obj.number) <2 or \
        loop_counter == 1 or loop_counter == paginator_obj.paginator.num_pages: #the first page or last

        return mark_safe('''<li><a href="{abs_url}">{page_num}</a></li>'''\
            .format(abs_url= url,page_num=loop_counter))
    elif abs(loop_counter - paginator_obj.number) <3:
        return mark_safe('''<li><a href="{abs_url}">...</a></li>'''\
            .format(abs_url=url ,page_num=loop_counter))
    else:
        return ''


@register.simple_tag
def pagenator(obj,data_type):
    html = '''<ul class="pagination">'''
    if obj.has_previous():
        html += '''<li class="disabled"><a href="?page=%s&type=%s" class="fa fa-angle-double-left"></a></li>''' %(obj.previous_page_number(),data_type)


    for p_num in obj.paginator.page_range:
        if p_num == obj.number:
            html += '''<li class="active"><a href="?page=%s&type=%s">%s</a></li>''' %(p_num,data_type,p_num)
        else:
            html += '''<li ><a href="?page=%s&type=%s">%s</a></li>''' %(p_num,data_type,p_num)
    if obj.has_next():
        html += '''<li class="disabled"><a href="?page=%s&type=%s" class="fa fa-angle-double-right"></a></li>''' %( obj.next_page_number(),data_type)

    html += "</ul>"

    return mark_safe(html)

@register.simple_tag
def pagenator2(obj,arg_name,arg_val):
    html = '''<ul class="pagination">'''
    if obj.has_previous():
        html += '''<li class="disabled"><a href="?page=%s&%s=%s" class="fa fa-angle-double-left"></a></li>''' %(obj.previous_page_number(),arg_name,arg_val)

    for p_num in obj.paginator.page_range:
        if p_num == obj.number:
            html += '''<li class="active"><a href="?page=%s&%s=%s">%s</a></li>''' %(p_num,arg_name,arg_val,p_num)
        else:
            html += '''<li ><a href="?page=%s&%s=%s">%s</a></li>''' %(p_num,arg_name,arg_val,p_num)
    if obj.has_next():
        html += '''<li class="disabled"><a href="?page=%s&%s=%s" class="fa fa-angle-double-right"></a></li>''' %( obj.next_page_number(),arg_name,arg_val)

    html += "</ul>"

    return mark_safe(html)

@register.filter
def get_range( value ):
  """
    Filter - returns a list containing range made from given value
    Usage (in template):

    <ul>{% for i in 3|get_range %}
      <li>{{ i }}. Do something</li>
    {% endfor %}</ul>

    Results with the HTML:
    <ul>
      <li>0. Do something</li>
      <li>1. Do something</li>
      <li>2. Do something</li>
    </ul>

    Instead of 3 one may use the variable set in the views
  """
  return range( value )


@register.filter
def int_to_str(value):
    return str(value)

@register.filter
def to_string(value):
    return '%s' %value


@register.simple_tag
def get_db_table_name(table_admin_class):
    #print("table_admin_class",table_admin_class.model)

    return table_admin_class.model._meta.verbose_name.capitalize()


@register.simple_tag
def get_attr(obj):
    #print("get attr:",dir(obj))
    pass

@register.simple_tag
def get_m2m_objs(rel_field_name, form_obj):
    #print("get_m2m_objs", [rel_field_name,form_obj])

    #return
    ##print("has attr m2m",hasattr(model_obj,rel_field_name))
    try:

        m2m_objs = getattr(form_obj.instance,rel_field_name)
        ##print("m2m objs:",m2m_objs)
        return m2m_objs.model.objects.all()
    except Exception as e :
        ##print("err",e)
        #teachers.rel.to.objects.all()
        m2m_field_obj = getattr(form_obj.Meta.model,rel_field_name)
        return  m2m_field_obj.rel.to.objects.all()
        #return model_obj._meta.model.bind_hosts.through.bindhosts.get_queryset()
        #return  # to deal ValueError: "<UserProfile: >" needs to have a value for field "userprofile" before this many-to-many relationship can be used.



@register.simple_tag
def load_admin_actions(table_obj):
    #print('---acitons',table_obj.admin_class)
    select_ele = "<select id='admin_action' name='admin_action' class='form-control' ><option value=''>----</option>"
    for option in table_obj.actions:
        action_display_name = option
        if hasattr(table_obj.admin_class, option):
            action_func = getattr(table_obj.admin_class,option)
            if hasattr(action_func,'short_description'):
                action_display_name = action_func.short_description
        select_ele += ("<option value='%s'>" % option) + action_display_name + "</options>"
    select_ele += "</select>"

    return mark_safe(select_ele)

@register.simple_tag
def check_disabled_attr(field_name,form_obj):
    if form_obj.Meta.form_create is True:
        return ''
    if field_name in form_obj.Meta.admin.readonly_fields:
        return 'disabled'

@register.simple_tag
def get_time_humanize_display(time_seconds):
    if time_seconds < 60:
        return '%s秒'%time_seconds
    elif time_seconds < 60*60:
        return '%s分' % (time_seconds/60)

    elif time_seconds < 60 * 60 * 24:
        return '%s小时' % (time_seconds /60/60)


@register.simple_tag
def get_chosen_m2m_objs(form_field_obj, model_obj):
    '''return chosen m2m objs'''
    selected_pks = form_field_obj.value()
    try :
        m2m_objs = getattr(model_obj,form_field_obj.name)
        selected_objs = m2m_objs.select_related().filter(id__in=selected_pks)
        ##print("get_chosen_m2m_objs", form_field_obj.value(), selected_objs)
        ##print(selected_objs.values())
        return selected_objs
    except ValueError as e :
        return []


@register.simple_tag
def add_fk_search_btn(form_obj,field):
    ##print("add_fk_search_btn",field)
    ##print("add_fk_search_btn",dir(field))
    ##print("form",form_obj.__dict__)
    ##print("---fields",form_obj.instance._meta.get_fields())
    for field_obj in form_obj.instance._meta.get_fields():
         ##print("=--",repr(field_obj))
         if field.name == field_obj.name:
             if 'ForeignKey' in repr(field_obj):
                 ##print('got fk ', field)
                 if field.name not in form_obj.Meta.admin.readonly_fields:

                     ele = '''
                        <i style="cursor: pointer" data-target="#modal-dialog" data-toggle="modal"
                        class="fa fa-search" aria-hidden="true"
                        onclick="PrepareFilterSearch('%s')"></i>'''% field.name
                     return mark_safe(ele)
    return ''


@register.simple_tag
def add_onclick_link(form_obj,field_obj):
    '''
    在表的修改页面给配置好的change_page_onclick_field加link
    :param form_obj:
    :param field_obj:
    :return:
    '''
    if field_obj.name in form_obj.Meta.admin.change_page_onclick_fields:
        # link_url = url_reverse(form_obj.Meta.admin.change_page_onclick_fields[field_obj.name][0],
        #                        args=(form_obj.instance.id,))
        link_ele = '''<a class="btn-link" href="%s/" >%s</a>''' % \
                        (form_obj.Meta.admin.change_page_onclick_fields[field_obj.name][0],
                        form_obj.Meta.admin.change_page_onclick_fields[field_obj.name][1],
                         )
        return mark_safe(link_ele)
    return ''




def recursive_related_objs_lookup(objs):
    #model_name = objs[0]._meta.model_name
    ul_ele = "<ul>"
    for obj in objs:
        li_ele = '''<li><span class='btn-link'> %s:</span> %s </li>'''%(obj._meta.verbose_name,obj.__str__().strip("<>"))
        ul_ele += li_ele

        #for local many to many
        ##print("------- obj._meta.local_many_to_many", obj._meta.local_many_to_many)
        for m2m_field in obj._meta.local_many_to_many: #把所有跟这个对象直接关联的m2m字段取出来了
            sub_ul_ele = "<ul>"
            m2m_field_obj = getattr(obj,m2m_field.name) #getattr(customer, 'tags')
            for o in m2m_field_obj.select_related():# customer.tags.select_related()
                li_ele = '''<li> %s: %s </li>''' % (m2m_field.verbose_name, o.__str__().strip("<>"))
                sub_ul_ele +=li_ele

            sub_ul_ele += "</ul>"
            ul_ele += sub_ul_ele  #最终跟最外层的ul相拼接


        for related_obj in obj._meta.related_objects:
            if 'ManyToManyRel' in related_obj.__repr__():

                if hasattr(obj, related_obj.get_accessor_name()):  # hassattr(customer,'enrollment_set')
                    accessor_obj = getattr(obj, related_obj.get_accessor_name())
                    #print("-------ManyToManyRel",accessor_obj,related_obj.get_accessor_name())
                    # 上面accessor_obj 相当于 customer.enrollment_set
                    if hasattr(accessor_obj, 'select_related'):  # slect_related() == all()
                        target_objs = accessor_obj.select_related()  # .filter(**filter_coditions)
                        # target_objs 相当于 customer.enrollment_set.all()

                        sub_ul_ele ="<ul style='color:red'>"
                        for o in target_objs:
                            li_ele = '''<li> <span class='btn-link'>%s</span>: %s </li>''' % (o._meta.verbose_name, o.__str__().strip("<>"))
                            sub_ul_ele += li_ele
                        sub_ul_ele += "</ul>"
                        ul_ele += sub_ul_ele

            elif hasattr(obj,related_obj.get_accessor_name()): # hassattr(customer,'enrollment_set')
                accessor_obj = getattr(obj,related_obj.get_accessor_name())
                #上面accessor_obj 相当于 customer.enrollment_set
                if hasattr(accessor_obj,'select_related'): # slect_related() == all()
                    target_objs = accessor_obj.select_related() #.filter(**filter_coditions)
                    # target_objs 相当于 customer.enrollment_set.all()
                else:
                    #print("one to one i guess:",accessor_obj)
                    target_objs = [accessor_obj]
                #print("target_objs",target_objs)
                if len(target_objs) >0:
                    ##print("\033[31;1mdeeper layer lookup -------\033[0m")
                    #nodes = recursive_related_objs_lookup(target_objs,model_name)
                    nodes = recursive_related_objs_lookup(target_objs)
                    ul_ele += nodes
    ul_ele +="</ul>"
    return ul_ele



def recursive_related_objs_lookup_old(objs,model_name):
    model_name = objs[0]._meta.model_name
    ul_ele = "<ul>"
    for obj in objs:
        # li_ele = '''<li>
        #     <a href="/configure/web_hosts/change/%s/" >%s</a> </li>''' % (obj.id,obj.__repr__().strip("<>"))
        # ul_ele += li_ele
        # #print("-----li",li_ele)
        li_ele = '''<li> %s: %s </li>'''%(obj._meta.verbose_name,obj.__str__().strip("<>"))
        ul_ele +=li_ele
        for related_obj in obj._meta.related_objects:
            if 'ManyToOneRel' not in related_obj.__repr__():
                continue
            if hasattr(obj,related_obj.get_accessor_name()):
                accessor_obj = getattr(obj,related_obj.get_accessor_name())

                if hasattr(accessor_obj,'select_related'):
                    target_objs = accessor_obj.select_related() #.filter(**filter_coditions)

                else:
                    ##print("one to one i guess:",accessor_obj)
                    target_objs = accessor_obj
                if len(target_objs) >0:
                    ##print("\033[31;1mdeeper layer lookup -------\033[0m")
                    nodes = recursive_related_objs_lookup(target_objs,model_name)
                    ul_ele += nodes
    ul_ele +="</ul>"
    return ul_ele

@register.simple_tag
def display_obj_related(objs):
    '''把对象及所有相关联的数据取出来'''
    if objs:
        model_class = objs[0]._meta.model
        #mode_name = objs[0]._meta.model_name
        return mark_safe(recursive_related_objs_lookup(objs))



