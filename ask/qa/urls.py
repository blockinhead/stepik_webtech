from django.conf.urls import url
from django.contrib import admin
from .views import question_details

urlpatterns = [
    # url(r'^admin/', admin.site.urls),
    url(r'^(?P<pk>\d+)/$', question_details, name='question_details'),
]