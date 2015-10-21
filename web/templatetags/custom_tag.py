#_*_coding:utf-8_*_
__author__ = 'jieli'
import datetime

from django import template
from web import models
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

    return html

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

    return html

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

    print '--->str',value
    return str(value)