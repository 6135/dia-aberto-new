import django_filters
from django.db.models import Exists, OuterRef
import datetime
from configuracao.models import *
from atividades.models import Tema
from django.forms.widgets import TextInput

class TemaFilter(django_filters.FilterSet):
    tema = django_filters.CharFilter(
        field_name="tema", lookup_expr='icontains')

    class Meta:
        model = Tema
        fields = '__all__'

def get_faculdades(queryset, name, value):
    return queryset.filter(
        Exists(Curso.objects.filter(
            id=OuterRef('pk'),
            unidadeorganicaid=value
        ))
    )

class CursoFilter(django_filters.FilterSet):
    nome = django_filters.CharFilter(
        field_name="nome", lookup_expr='icontains')
    sigla = django_filters.CharFilter(
        field_name="sigla", lookup_expr='icontains')
    unidadeorganicaid = django_filters.CharFilter(method=get_faculdades)

    class Meta:
        model = Curso
        fields = '__all__'

def get_faculdades_dep(queryset, name, value):
    return queryset.filter(
        Exists(Departamento.objects.filter(
            id=OuterRef('pk'),
            unidadeorganicaid=value
        ))
    )

class DepartamentoFilter(django_filters.FilterSet):
    nome = django_filters.CharFilter(
        field_name="nome", lookup_expr='icontains')
    sigla = django_filters.CharFilter(
        field_name="sigla", lookup_expr='icontains')
    unidadeorganicaid = django_filters.CharFilter(method=get_faculdades_dep)

    class Meta:
        model = Departamento
        fields = '__all__'

def get_campi(queryset, name, value):
    return queryset.filter(
        Exists(Edificio.objects.filter(
            id=OuterRef('pk'),
            campus_id=value
        ))
    )

class EdificioFilter(django_filters.FilterSet):
    nome = django_filters.CharFilter(
        field_name="nome", lookup_expr='icontains')
    campus = django_filters.CharFilter(method=get_campi)

    class Meta:
        model = Edificio
        fields = ['nome', 'campus']


class UOFilter(django_filters.FilterSet):
    nome = django_filters.CharFilter(
        field_name="nome", lookup_expr='icontains')
    sigla = django_filters.CharFilter(
        field_name="sigla", lookup_expr='icontains')   
    campusis = django_filters.CharFilter(method=get_campi)

    class Meta:
        model = Unidadeorganica
        fields = ['nome','sigla', 'campusid']

def get_campi_menu(queryset,name,value):
    return queryset.filter(
        Exists(Menu.objects.filter(
            id=OuterRef('pk'),
            campus=value
        ))
    )    
class MenuFilter(django_filters.FilterSet):
    dia = django_filters.DateFilter(field_name="dia")
    campus = django_filters.CharFilter(method=get_campi)

    class Meta:
        model = Menu
        fields = ['campus', 'dia']