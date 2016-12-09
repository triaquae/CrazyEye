#_*_coding:utf-8_*_
__author__ = 'jieli'
import datetime
import re
from django import template
from web import models
from django.utils.safestring import mark_safe
from  django.core.urlresolvers import reverse as url_reverse

register = template.Library()


@register.simple_tag
def current_time1(format_string):
    return format_string.upper()

@register.simple_tag(takes_context=True)
def current_time(context, format_string):
    timezone = context['timezone']
    return your_get_current_time_method(timezone, format_string)

@register.simple_tag
#def filter_table(table, field, *args, **kwargs):
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
    print(table_obj.model_class)
    return  table_obj.model_class._meta.get_field(column).verbose_name


@register.simple_tag
def load_search_element(table_obj):
    print("search:",table_obj.search_fields)
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
    for index,column_name in enumerate(table_obj.list_display):


        field_obj = row_obj._meta.get_field(column_name)
        column_data = field_obj._get_val_from_obj(row_obj)
        if column_name in table_obj.choice_fields:
            column_data = getattr(row_obj,'get_%s_display'%column_name)()
        if column_name in table_obj.fk_fields:
            column_data = getattr(row_obj,column_name).__str__()
        if 'DateTimeField' in field_obj.__repr__():
            column_data = getattr(row_obj,column_name).strftime( "%Y-%m-%d %H:%M:%S") \
                    if getattr(row_obj,column_name) else None
        if 'ManyToManyField' in field_obj.__repr__():
            column_data = getattr(row_obj, column_name).select_related().count()
        if onclick_column == column_name:
            column = ''' <td><a class='btn-link' href=%s>%s</a></td> '''% (url_reverse(target_link,args=(column_data, )),column_data)
        if column_name in table_obj.onclick_fields:
            column = '''<td><a class='btn-link' href='%s' target='_blank'>%s</a></td>''' % \
                     (url_reverse(table_obj.onclick_fields[column_name],args=(row_obj.id, )), column_data)

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


        row_ele +=column
    #for dynamic display
    if table_obj.dynamic_fk :
        if hasattr(row_obj,table_obj.dynamic_fk ):
            #print("----dynamic:",getattr(row_obj,table_obj.dynamic_fk), row_obj)
            #print(row_obj.networkdevice)
            dy_fk = getattr(row_obj,table_obj.dynamic_fk) #拿到的是asset_type的值
            if hasattr(row_obj,dy_fk):
                dy_fk_obj = getattr(row_obj,dy_fk)
                print("-->type",type(dy_fk_obj), dy_fk_obj )
                for index,column_name in enumerate(table_obj.dynamic_list_display):
                    if column_name in table_obj.dynamic_choice_fields:
                        column_data = getattr(dy_fk_obj, 'get_%s_display' % column_name)()
                    else:
                        column_data = dy_fk_obj._meta.get_field(column_name)._get_val_from_obj(dy_fk_obj)
                    print("dynamic column data", column_data)

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
    print("table_admin_class",table_admin_class.model)

    return table_admin_class.model._meta.verbose_name


@register.simple_tag
def get_attr(obj):
    print("get attr:",dir(obj))


@register.simple_tag
def get_m2m_objs(rel_field_name, model_obj):
    print("get_m2m_objs", [rel_field_name,model_obj], model_obj._meta.label)
    #print("has attr m2m",hasattr(model_obj,rel_field_name))
    try:

        m2m_objs = getattr(model_obj,rel_field_name)
        print("m2m objs:",m2m_objs)
        return m2m_objs.model.objects.all()
    except ValueError as e :
        #print(e)
        return model_obj._meta.model.bind_hosts.through.bindhosts.get_queryset()
        #return  # to deal ValueError: "<UserProfile: >" needs to have a value for field "userprofile" before this many-to-many relationship can be used.


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
        #print("get_chosen_m2m_objs", form_field_obj.value(), selected_objs)
        #print(selected_objs.values())
        return selected_objs
    except ValueError as e :
        return []


@register.simple_tag
def add_fk_search_btn(form_obj,field):
    #print("add_fk_search_btn",field)
    #print("add_fk_search_btn",dir(field))
    #print("form",form_obj.__dict__)
    #print("---fields",form_obj.instance._meta.get_fields())
    for field_obj in form_obj.instance._meta.get_fields():
         #print("=--",repr(field_obj))
         if field.name == field_obj.name:
             if 'ForeignKey' in repr(field_obj):
                 #print('got fk ', field)
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
        link_ele = '''<a class="btn-link" href="password/" >%s</a>''' % \
                        (form_obj.Meta.admin.change_page_onclick_fields[field_obj.name][1])
        return mark_safe(link_ele)
    return ''
# @register.simple_tag
# def decorate_date_field(form_obj,field_obj):
#     print("repr...",field_obj)
#     #print("repr.field..",dir(field_obj.field))
#     field_type = repr(form_obj.Meta.model._meta.get_field(field_obj.name))
#     filed_val = getattr(form_obj.instance,field_obj.name)
#     if 'DateTimeField' in field_type:
#         field_ele = '''
#
#         <div style="margin-left:-10px" class="col-md-7 dp-component">
#             <div class="input-group date">
#                 <input id="id_%s" name="%s" type="text"  value="%s" class="form-control">
#                 <span class="input-group-addon"><i class="fa fa-calendar fa-lg"></i></span>
#
#             </div>
#         </div>
#         <div class="col-md-5 input-group date">
#             <input class="tp-textinput form-control" type="text" >
#             <span class="input-group-addon"><i class="fa fa-clock-o fa-lg"></i></span>
#         </div>
#         '''%(field_obj.name,field_obj.name,filed_val)
#         return mark_safe(field_ele)


