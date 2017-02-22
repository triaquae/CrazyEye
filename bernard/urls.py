
from django.conf.urls import include, url

from bernard import views
urlpatterns = [

    url(r'test/$',views.task_test),
    url(r'schedule_index/$',views.schedule_index,name="schedule_index"),
    url(r'plan/(\d+)/$',views.plan_detail,name="plan_detail"),
    url(r'task_order/(\d+)/$',views.save_task_order,name="save_task_order"),

]
