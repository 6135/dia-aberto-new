from django.shortcuts import render
from django.core.exceptions import ValidationError
from .forms import *
from utilizadores.forms import ParticipanteForm
from django.http.request import HttpRequest
from django.views.generic.edit import CreateView
from .models import *



