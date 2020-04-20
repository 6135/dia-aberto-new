from django.urls import path
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^adicionartarefa/$',views.adicionartarefa,name="adicionarTarefa"),
    url(r'^consultartarefa/$',views.consultartarefa,name="consultarTarefa"),
]
