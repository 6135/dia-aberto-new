from django.urls import path
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^adicionartarefa/$',views.adicionartarefa,name="adicionarTarefa"),
    url(r'^consultartarefa/$',views.consultartarefa,name="consultarTarefa"),
    url(r'^ajax/adicionarsessoes/$', views.sessoesAtividade, name='sessoesAtividade'),
    url(r'^ajax/adicionardias/$', views.diasAtividade, name='diasAtividade'),
    url(r'^ajax/adicionarcolaboradores/$', views.colaboradoresAtividade, name='colaboradoresAtividade'),
    url(r'^ajax/tipotarefa/$', views.tipoTarefa, name='tipoTarefa'),
    url(r'^ajax/grupoinfo/$', views.grupoInfo, name='grupoInfo'),
    url(r'^ajax/diasgrupo/$', views.diasGrupo, name='diasGrupo'),
    url(r'^ajax/horariogrupo/$', views.horarioGrupo, name='horarioGrupo'),
    path("eliminartarefa/<int:id>",views.eliminartarefa,name="eliminarTarefa"),
    path("atribuircolaborador/<int:tarefa>",views.atribuircolaborador,name="atribuirColaborador"),
]
