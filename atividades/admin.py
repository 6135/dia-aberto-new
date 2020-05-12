from django.contrib import admin
from .models import Atividade, Sessao, Tema, Materiais,Anfiteatro
from configuracao.models import Espaco, Edificio, Diaaberto, Horario

admin.site.register(Atividade)
admin.site.register(Sessao)
admin.site.register(Tema)
admin.site.register(Materiais)
admin.site.register(Anfiteatro)
admin.site.register(Espaco)
admin.site.register(Edificio)
admin.site.register(Diaaberto)
admin.site.register(Horario)
# Register your models here.
