from django.urls import path
from django.conf.urls import url
from . import views

app_name = 'coordenadores'

urlpatterns = [
    path('adicionartarefa/',views.adicionartarefa,name="adicionarTarefa"),
    path('alterartarefa/<int:id>',views.adicionartarefa,name="alterarTarefa"),
    url(r'^consultartarefa/$',views.ConsultarTarefas.as_view(),name="consultarTarefa"),
    url(r'^ajax/adicionarsessoes/$', views.sessoesAtividade, name='sessoesAtividade'),
    url(r'^ajax/adicionardias/$', views.diasAtividade, name='diasAtividade'),
    url(r'^ajax/adicionarcolaboradores/$', views.colaboradores, name='colaboradores'),
    url(r'^ajax/tipotarefa/$', views.tipoTarefa, name='tipoTarefa'),
    url(r'^ajax/grupoinfo/$', views.grupoInfo, name='grupoInfo'),
    url(r'^ajax/diasgrupo/$', views.diasGrupo, name='diasGrupo'),
    url(r'^ajax/horariogrupo/$', views.horarioGrupo, name='horarioGrupo'),
    url(r'^ajax/origemgrupo/$', views.locaisOrigem, name='locaisOrigem'),
    url(r'^ajax/destinogrupo/$', views.locaisDestino, name='locaisDestino'),
    url('eliminartarefa/<int:id>',views.eliminartarefa,name="eliminarTarefa"),
    #path("atribuircolaborador/<int:tarefa>",views.atribuircolaborador,name="atribuirColaborador"),
]
