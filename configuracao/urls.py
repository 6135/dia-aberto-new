from django.contrib import admin
from django.urls import path
from . import views
urlpatterns = [
    path("",views.homepage,name="inicio"),
    path('admin', views.homepage, name='adminpage'),
    path('diasabertos', views.viewDays, name='diasAbertos'),
    path("editardia/<int:id>", views.newDay, name='editarDia'),
    path('inserirdiaaberto', views.newDay,name='novoDia' )
]
