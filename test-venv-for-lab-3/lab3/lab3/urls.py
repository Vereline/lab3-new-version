"""lab3 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from trashes import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    # url(r'^$', views.trash_main(), name='trash_main'),
    url(r'^$', views.Main.as_view(), name='main'),
    url(r'^task_list/$', views.TaskList.as_view(), name='task_list'),
    url(r'^add_trash/$', views.AddTrash.as_view(), name='add_trash'),
    url(r'^add_task/$', views.AddTask.as_view(), name='add_task'),
    url(r'^delete_trash/(?P<pk>\d+)$', views.DeleteTrash.as_view(), name='delete_trash'),
    url(r'^refresh_trash/(?P<pk>\d+)$', views.RefreshTrash.as_view(), name='refresh_trash'),
    url(r'^delete_task/(?P<pk>\d+)$', views.DeleteTask.as_view(), name='delete_task'),
    url(r'^refresh_task/(?P<pk>\d+)$', views.RefreshTask.as_view(), name='refresh_task'),
    url(r'^define_action/(?P<name>[a-zA-Z0-9]+)$', views.define_action, name='define_action'),
    url(r'^define_action/remove/(?P<name>[a-zA-Z0-9]+)$', views.remove_file, name='remove'),
    url(r'^define_action/recover/(?P<name>[a-zA-Z0-9]+)$', views.recover_file, name='recover'),
    url(r'^task_list/do_the_task/(?P<pk>[a-zA-Z0-9]+)$', views.do_the_task, name='do_the_task'),

]
