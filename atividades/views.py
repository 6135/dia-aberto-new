from django.shortcuts import render, redirect
from .forms import AtividadeForm
from .models import Atividade


def atividade(request):
    if request.method == "POST":
        form = AtividadeForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                return redirect('/show')
            except:
                pass
    else:
        form = AtividadeForm()
    return render(request, 'atividades/index.html', {'form': form})


def show(request):
    Atividades = Atividade.objects.all()
    return render(request, "atividades/show.html", {'Atividades': Atividades})


def edit(request, id):
    Atividade = Atividade.objects.get(id=id)
    return render(request, 'atividades/edit.html', {'Atividade': Atividade})


def update(request, id):
    Atividade = Atividade.objects.get(id=id)
    form = AtividadeForm(request.POST, instance=Atividade)
    if form.is_valid():
        form.save()
        return redirect("/show")
    return render(request, 'atividades/edit.html', {'Atividade': Atividade})


def destroy(request, id):
    Atividade = Atividade.objects.get(id=id)
    Atividade.delete()
    return redirect("/show")
