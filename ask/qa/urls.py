from django.conf.urls import url
from django.contrib import admin
from .views import test

urlpatterns = [
    # url(r'^admin/', admin.site.urls),
    url(r'^(\d+)/$', test),
]