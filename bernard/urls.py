
from django.conf.urls import include, url

from bernard import views
urlpatterns = [

    url(r'test/$',views.task_test),
    url(r'schedule_index/$',views.schedule_index,name="schedule_index"),

]
