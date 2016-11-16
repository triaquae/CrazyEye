# _*_coding:utf-8_*_

from django.utils import timezone
from django.db.models import Count


def get_orderby(request, model_objs, admin_form):
    orderby_field = request.GET.get('orderby')
    if orderby_field:
        orderby_field = orderby_field.strip()
        orderby_column_index = admin_form.list_display.index(orderby_field.strip('-'))
        objs = model_objs.order_by(orderby_field)
        # print("orderby",orderby_field)
        if orderby_field.startswith('-'):
            orderby_field = orderby_field.strip('-')
        else:
            orderby_field = '-%s' % orderby_field

        return [objs, orderby_field, orderby_column_index]
    else:
        return [model_objs, orderby_field, None]


class TableHandler(object):
    def __init__(self, request, model_class, admin_class, query_sets, order_res):
        self.request = request
        self.model_class = model_class
        # self.admin_class = admin_class
        self.query_sets = query_sets
        self.choice_fields = admin_class.choice_fields
        self.fk_fields = admin_class.fk_fields

        self.list_display = admin_class.list_display
        self.list_filter = self.get_list_filter(admin_class.list_filter)

        # for order by
        self.orderby_field = order_res[1]
        self.orderby_col_index = order_res[2]

        # print("list display:",admin_class.list_display)

        self.colored_fields = getattr(admin_class,'colored_fields') if \
                hasattr(admin_class,'colored_fields') else {}


        #for dynamic display
        self.dynamic_fk = getattr(admin_class,'dynamic_fk') if \
                hasattr(admin_class, 'dynamic_fk') else None
        self.dynamic_list_display = getattr(admin_class,'dynamic_list_display') if \
            hasattr(admin_class,'dynamic_list_display') else ()
        self.dynamic_choice_fields = getattr(admin_class,'dynamic_choice_fields') if \
            hasattr(admin_class,'dynamic_choice_fields') else ()
    def get_list_filter(self, list_filter):
        filters = []
        # print("list filters",list_filter)
        for i in list_filter:
            col_obj = self.model_class._meta.get_field(i)
            # print("col obj", col_obj)
            data = {
                'verbose_name': col_obj.verbose_name,
                'column_name': i,
                # 'choices' : col_obj.get_choices()
            }
            if col_obj.deconstruct()[1] not in ('django.db.models.DateField','django.db.models.DateTimeField'):
                try:
                    choices = col_obj.get_choices()

                except AttributeError as e:
                    choices_list = col_obj.model.objects.values(i).annotate(count=Count(i))
                    choices = [[obj[i], obj[i]] for obj in choices_list]
                    choices.insert(0, ['', '----------'])
            else:  # 特殊处理datefield
                today_obj = timezone.datetime.now()
                choices = [
                    ('', '---------'),
                    (today_obj.strftime("%Y-%m-%d"), '今天'),
                    ((today_obj - timezone.timedelta(days=7)).strftime("%Y-%m-%d"), '过去7天'),
                    ((today_obj - timezone.timedelta(days=today_obj.day)).strftime("%Y-%m-%d"), '本月'),
                    ((today_obj - timezone.timedelta(days=90)).strftime("%Y-%m-%d"), '过去3个月'),
                    ((today_obj - timezone.timedelta(days=180)).strftime("%Y-%m-%d"), '过去6个月'),
                    ((today_obj - timezone.timedelta(days=365)).strftime("%Y-%m-%d"), '过去1年'),
                ]
                print(choices)
            data['choices'] = choices

            # handle selected data
            if self.request.GET.get(i):
                data['selected'] = self.request.GET.get(i)
            filters.append(data)
        # print(filters)

        return filters


def table_filter(request, model_admin, models_class):
    '''根据过滤条件查找数据'''

    print(model_admin.list_filter)
    filter_conditions = {}
    for condition in model_admin.list_filter:
        if request.GET.get(condition):
            filed_type_name = models_class._meta.get_field(condition).__repr__()
            print("filed_type_name",filed_type_name)
            if 'ForeignKey' in filed_type_name:
                filter_conditions['%s_id' % condition] = request.GET.get(condition)
            elif 'DateField' in filed_type_name or 'DateTimeField' in filed_type_name:
                filter_conditions['%s__gt' % condition] = request.GET.get(condition)
            else:
                filter_conditions[condition] = request.GET.get(condition)

    print("filter conditons", filter_conditions)
    return models_class.objects.filter(**filter_conditions)
