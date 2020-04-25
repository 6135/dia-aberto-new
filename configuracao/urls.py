from django.contrib import admin
from django.urls import path
from . import views
urlpatterns = [
    path("",views.homepage,name="inicio"),
    path('admin', views.homepage, name='adminpage'),
    path('diasabertos', views.viewDays, name='diasAbertos'),
    path('editardia/<int:id>', views.newDay, name='editarDia'),
    path('inserirdiaaberto', views.newDay,name='novoDia' ),
    path('deldia/<int:id>', views.delDay, name='eliminarDia'),
    path('daysjson', views.view_days_as_json, name='daysjson'),
    path('menus',views.viewMenus, name='verMenus'),
    path('delmenu/<int:id>', views.delMenu, name='eliminarMenu'),
    path('editarmenu/<int:id>',views.newMenu, name='editarMenu'),
    path('novomenu', views.newMenu, name='novoMenu'),
    path('adicionarprato/<int:id>', views.newPrato, name='novoPrato'),
    path('delprato/<int:id>', views.delPrato, name='eliminarPrato'),
    path('ajax/getDias', views.getDias, name='getDias'),

]
