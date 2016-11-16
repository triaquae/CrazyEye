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
        column_data = row_obj._meta.get_field(column_name)._get_val_from_obj(row_obj)
        if column_name in table_obj.choice_fields:
            column_data = getattr(row_obj,'get_%s_display'%column_name)()
        if column_name in table_obj.fk_fields:
            column_data = getattr(row_obj,column_name).__str__()
        if onclick_column == column_name:
            column = ''' <td><a href=%s>%s</a></td> '''% (url_reverse(target_link,args=(column_data, )),column_data)
        if column_name in table_obj.colored_fields: #特定字段需要显示color

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
