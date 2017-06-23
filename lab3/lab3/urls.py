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
    url(r'^add_trash/$', views.AddTrash.as_view(), name='add_trash'),
    url(r'^refresh_trash/(?P<pk>\d+)$', views.RefreshTrash.as_view(), name='refresh_trash'),
]
