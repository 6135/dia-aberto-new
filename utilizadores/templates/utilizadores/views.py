from django.shortcuts import render
from django.http import HttpResponse
from .models import Utilizador, ProfessorUniversitario, Participante, Colaborador, Coordenador
from django.shortcuts import redirect
from .forms import *
from django.contrib import messages
from django.contrib.auth import *
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.models import Group

from configuracao.models import Unidadeorganica,Departamento,Curso


from django.core.paginator import Paginator


def load_departamentos(request):
    faculdadeid = request.GET.get('faculdade')
    departamentos = Departamento.objects.filter(unidadeorganicaid=faculdadeid).order_by('nome')
    return render(request, 'utilizadores/departamento_dropdown_list_options.html', {'departamentos': departamentos})

def load_cursos(request):
    faculdadeid = request.GET.get('faculdade')
    cursos = Curso.objects.filter(unidadeorganicaid=faculdadeid).order_by('nome')
    return render(request, 'utilizadores/curso_dropdown_list_options.html', {'cursos': cursos})


def consultar_utilizadores(request):
        
    if request.user.is_authenticated:    
        user = get_user(request)
        if user.groups.filter(name = "Coordenador").exists():
            u = "Coordenador"
        elif user.groups.filter(name = "Administrador").exists():
            u = "Administrador"
        else:
            return redirect('utilizadores:mensagem',5)
    else:
        return redirect('utilizadores:mensagem',5)  


    if request.method == 'POST':
        formFilter = UtilizadorFiltro(request.POST)
        current = request.POST.get('current')

        form = formFilter
        tipo_utilizadores = request.POST.get('filtro_tipo')
        estado_utilizadores = request.POST.get('filtro_estado')
        txt = request.POST.get('current')

        if estado_utilizadores != "":
            if estado_utilizadores == "T":
                estado = 'True'
            elif estado_utilizadores == "F":
                estado = 'False'
            elif estado_utilizadores == "R":
                estado = 'Rejeitado'    
            else:
                estado = 'True'
        else:
            estado = 'True'

        if txt != "":
            nome = txt.split()
            sz = len(nome)
            if sz == 1:
                if estado_utilizadores != "":
                    utilizadores = Utilizador.objects.filter(
                        valido=estado, first_name=current)
                else:
                    utilizadores = Utilizador.objects.filter(
                        first_name=current)
                if len(utilizadores) == 0:
                    if estado_utilizadores != "":
                        utilizadores = Utilizador.objects.filter(
                            valido=estado, last_name=current)
                    else:
                        utilizadores = Utilizador.objects.filter(
                            last_name=current)
            else:
                if estado_utilizadores != "":
                    utilizadores = Utilizador.objects.filter(valido=estado, first_name=nome[0]).filter(
                        valido=estado, last_name=nome[1]).order_by('first_name')
                else:
                    utilizadores = Utilizador.objects.filter(first_name=nome[0]).filter(
                        last_name=nome[1]).order_by('first_name')
        elif estado_utilizadores == "":
            if tipo_utilizadores == "Utilizador":
                utilizadores = Utilizador.objects.all().order_by('first_name')
            elif tipo_utilizadores == "Participante":
                utilizadores = Participante.objects.all().order_by('first_name')
            elif tipo_utilizadores == "ProfessorUniversitario":
                utilizadores = ProfessorUniversitario.objects.all().order_by('first_name')
            elif tipo_utilizadores == "Coordenador":
                utilizadores = Coordenador.objects.all().order_by('first_name')
            elif tipo_utilizadores == "Colaborador":
                utilizadores = Colaborador.objects.all().order_by('first_name')
        else:
            if tipo_utilizadores == "Utilizador":
                utilizadores = Utilizador.objects.filter(
                    valido=estado).order_by('first_name')
            elif tipo_utilizadores == "Participante":
                utilizadores = Participante.objects.filter(
                    valido=estado).order_by('first_name')
            elif tipo_utilizadores == "ProfessorUniversitario":
                utilizadores = ProfessorUniversitario.objects.filter(
                    valido=estado).order_by('first_name')
            elif tipo_utilizadores == "Coordenador":
                utilizadores = Coordenador.objects.filter(
                    valido=estado).order_by('first_name')
            elif tipo_utilizadores == "Colaborador":
                utilizadores = Colaborador.objects.filter(
                    valido=estado).order_by('first_name')
    else:
        formFilter = UtilizadorFiltro()
        current = ""
        utilizadores = Utilizador.objects.all().order_by('first_name')
        form = formFilter
    
    paginator= Paginator(utilizadores,5)
    page=request.GET.get('page')
    utilizadores = paginator.get_page(page)
    return render(request=request, template_name='utilizadores/consultar_utilizadores.html', context={"utilizadores": utilizadores, 'form': form, 'current': current, 'u': u})


def escolher_perfil(request):
    if request.user.is_authenticated:    
        user = get_user(request)
        if user.groups.filter(name = "Coordenador").exists():
            u = "Coordenador"
        elif user.groups.filter(name = "Administrador").exists():
            u = "Administrador"
        elif user.groups.filter(name = "ProfessorUniversitario").exists():
            u = "ProfessorUniversitario"
        elif user.groups.filter(name = "Colaborador").exists():
            u = "Colaborador"
        elif user.groups.filter(name = "Participante").exists():
            u = "Participante" 
        else:
            u=""     
    else:
        u=""
    utilizadores = ["Participante",
                    "Professores Universitario", "Coordenador", "Colaborador","Administrador"]
    return render(request=request, template_name='utilizadores/escolher_perfil.html', context={"utilizadores": utilizadores,'u': u})


def criar_utilizador(request, id):
    if request.user.is_authenticated:    
        user = get_user(request)
        if user.groups.filter(name = "Coordenador").exists():
            u = "Coordenador"
        elif user.groups.filter(name = "Administrador").exists():
            u = "Administrador"
        elif user.groups.filter(name = "ProfessorUniversitario").exists():
            u = "ProfessorUniversitario"
        elif user.groups.filter(name = "Colaborador").exists():
            u = "Colaborador"
        elif user.groups.filter(name = "Participante").exists():
            u = "Participante" 
        else:
            u=""     
    else:
        u=""
    
    msg=False
    if request.method == "POST":
        tipo = id
        if tipo == 1:
            form = ParticipanteRegisterForm(request.POST)
            perfil = "Participante"
            my_group = Group.objects.get(name='Participante') 
        elif tipo == 2:
            form = ProfessorUniversitarioRegisterForm(request.POST)
            perfil = "Professor Universitario"
            my_group = Group.objects.get(name='ProfessorUniversitario')
        elif tipo == 3:
            form = CoordenadorRegisterForm(request.POST)
            perfil = "Coordenador"
            my_group = Group.objects.get(name='Coordenador')
        elif tipo == 4:
            form = ColaboradorRegisterForm(request.POST)
            perfil = "Colaborador"
            my_group = Group.objects.get(name='Colaborador')
        elif tipo == 5:
            form = AdministradorRegisterForm(request.POST)
            perfil = "Administrador"
            my_group = Group.objects.get(name='Administrador')    
        else:
            return redirect("utilizadores:escolher-perfil")

        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            first_name = form.cleaned_data.get('first_name')
            my_group.user_set.add(user)

            if tipo == 1:
                user.valido = 'True'
                user.save()
                p=1
            else:
                user.valido = 'False'
                user.save()
                p=0
            return redirect("utilizadores:concluir-registo",p)
        else:
            msg=True
            tipo = id
            return render(request=request,
                          template_name="utilizadores/criar_utilizador.html",
                          context={"form": form, 'perfil': perfil, 'u': u,'registo' : tipo,'msg': msg})
    else:
        tipo = id
        if tipo == 1:
            form = ParticipanteRegisterForm()
            perfil = "Participante"
        elif tipo == 2:
            form = ProfessorUniversitarioRegisterForm()
            perfil = "Professor Universitario"
        elif tipo == 3:
            form = CoordenadorRegisterForm()
            perfil = "Coordenador"
        elif tipo == 4:
            form = ColaboradorRegisterForm()
            perfil = "Colaborador"
        elif tipo == 5:
            form = ColaboradorRegisterForm()
            perfil = "Administrador" 
        else:
            return redirect("utilizadores:escolher-perfil")
    return render(request=request,
                  template_name="utilizadores/criar_utilizador.html",
                  context={"form": form, 'perfil': perfil,'u': u,'registo' : tipo,'msg': msg})


def login_action(request):
    if request.user.is_authenticated:    
        user = get_user(request)
        if user.groups.filter(name = "Coordenador").exists():
            u = "Coordenador"
        elif user.groups.filter(name = "Administrador").exists():
            u = "Administrador"
        elif user.groups.filter(name = "ProfessorUniversitario").exists():
            u = "ProfessorUniversitario"
        elif user.groups.filter(name = "Colaborador").exists():
            u = "Colaborador"
        elif user.groups.filter(name = "Participante").exists():
            u = "Participante" 
        else:
            u=""     
    else:
        u=""
    msg=False
    error=""
    if request.method == 'POST':
        form = LoginForm(request=request, data=request.POST)
        username = request.POST.get('username')
        password = request.POST.get('password')
        if username=="" or password=="":
                msg=True
                error="Todos os campos são obrigatórios!"
        else:
            user = authenticate(username=username, password=password)
            if user is not None:
                utilizador = Utilizador.objects.get(id=user.id)
                if utilizador.valido=="False": 
                    return redirect('utilizadores:mensagem',9)
                elif utilizador.valido=="Rejeitado":
                    return redirect('utilizadores:mensagem',10)
                else:
                    login(request, user)
                    return redirect('utilizadores:mensagem',1)
            else:
                msg=True
                error="O nome de utilizador ou a palavra-passe inválidos!"
    form = LoginForm()
    return render(request=request,
                  template_name="utilizadores/login.html",
                  context={"form": form,"msg": msg, "error": error, 'u': u})


def logout_action(request):
    logout(request)
    return redirect('utilizadores:mensagem',2)


def alterar_password(request):
    if request.user.is_authenticated:    
        user = get_user(request)
        if user.groups.filter(name = "Coordenador").exists():
            u = "Coordenador"
        elif user.groups.filter(name = "Administrador").exists():
            u = "Administrador"
        elif user.groups.filter(name = "ProfessorUniversitario").exists():
            u = "ProfessorUniversitario"
        elif user.groups.filter(name = "Colaborador").exists():
            u = "Colaborador"
        elif user.groups.filter(name = "Participante").exists():
            u = "Participante" 
        else:
            u=""     
    else:
        u=""
    msg=False
    error="" 
    if request.method == 'POST':
        form = AlterarPasswordForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return redirect('utilizadores:mensagem',6)
        else:
            msg=True
            error="Passwords Incorretas!"
    form = AlterarPasswordForm(user=request.user)
    return render(request=request,
                  template_name="utilizadores/alterar_password.html",
                  context={"form": form,"msg": msg, "error": error, 'u': u})    



def rejeitar_utilizador(request, id): 
    if request.user.is_authenticated:    
        user = get_user(request)
        if user.groups.filter(name = "Administrador").exists():
            u = "Administrador"   
        elif user.groups.filter(name = "Coordenador").exists():
            u = "Coordenador"       
        else:
            return redirect('utilizadores:mensagem',5) 
    else:
        return redirect('utilizadores:mensagem',5) 
        
    try:
        u = Utilizador.objects.get(id = id)
        u.valido = 'Rejeitado'           
        u.save()   
        subject = 'Validação do registo do na plataforma do dia aberto'
        message = 'Caro(a) '+u.first_name+",\n\n"
        message+='O seu registo na plataforma do dia aberto foi rejeitado!'+"\n\n"
        message+='Equipa do dia aberto da Ualg'
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [u.email,]
        send_mail( subject, message, email_from, recipient_list )


    except User.DoesNotExist:
        return redirect('utilizadores:mensagem',5)

    except Exception as e: 
        return redirect('utilizadores:mensagem',5)

    return redirect('utilizadores:consultar-utilizadores')

def alterar_idioma(request):   
     return redirect('utilizadores:mensagem',5)  

def validar_utilizador(request, id): 
    if request.user.is_authenticated:    
        user = get_user(request)
        if user.groups.filter(name = "Administrador").exists():
            u = "Administrador"   
        elif user.groups.filter(name = "Coordenador").exists():
            u = "Coordenador"       
        else:
            return redirect('utilizadores:mensagem',5) 
    else:
        return redirect('utilizadores:mensagem',5) 
        
    try:
        u = Utilizador.objects.get(id = id)
        u.valido = 'True'           
        u.save()   
        subject = 'Validação do registo do na plataforma do dia aberto'
        message = 'Caro(a) '+u.first_name+"\n\n"
        message+='O seu registo na plataforma do dia aberto foi bem sucedido!'+",\n\n"
        message+='Equipa do dia aberto da Ualg'
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [u.email,]
        send_mail( subject, message, email_from, recipient_list )


    except User.DoesNotExist:
        return redirect('utilizadores:mensagem',5)

    except Exception as e: 
        return redirect('utilizadores:mensagem',5)

    return redirect('utilizadores:consultar-utilizadores')


def apagar_utilizador(request, id): 
    if request.user.is_authenticated:    
        user = get_user(request)
        if user.groups.filter(name = "Administrador").exists():
            u = "Administrador"   
        elif user.groups.filter(name = "Coordenador").exists():
            u = "Coordenador"       
        else:
            return redirect('utilizadores:mensagem',5) 
    else:
        return redirect('utilizadores:mensagem',5)


    user = User.objects.get(id=id)
    if user.groups.filter(name = "Coordenador").exists():
        u = Coordenador.objects.filter(id=id)
    elif user.groups.filter(name = "Administrador").exists():
        u = Administrador.objects.filter(id=id)
    elif user.groups.filter(name = "ProfessorUniversitario").exists():
        u = ProfessorUniversitario.objects.filter(id=id)
    elif user.groups.filter(name = "Colaborador").exists():
        u = Colaborador.objects.filter(id=id)
    elif user.groups.filter(name = "Participante").exists():
        u = Participante.objects.filter(id=id) 
    else:
        u= user     

    u.delete() 
    return redirect('utilizadores:consultar-utilizadores')   


def apagar_proprio_utilizador(request):  

    if request.user.is_authenticated:
        id=request.user.id  
        user = get_user(request)
        if user.groups.filter(name = "Coordenador").exists():
            u = Coordenador.objects.filter(id=id)
        elif user.groups.filter(name = "Administrador").exists():
            u = Administrador.objects.filter(id=id)
        elif user.groups.filter(name = "ProfessorUniversitario").exists():
            u = ProfessorUniversitario.objects.filter(id=id)
        elif user.groups.filter(name = "Colaborador").exists():
            u = Colaborador.objects.filter(id=id)
        elif user.groups.filter(name = "Participante").exists():
            u = Participante.objects.filter(id=id) 
        else:
            u= user     
    else:
        return redirect('utilizadores:mensagem',5)


    u.delete() 
    logout(request)
    return redirect('utilizadores:mensagem',7)   


def enviar_email_validar(request,nome,id):  
    msg="A enviar email a "+nome+" a informar que o seu registo foi validado"
    return render(request=request,
                  template_name="utilizadores/enviar_email_validar.html",
                  context={"msg": msg, "id":id})

def enviar_email_rejeitar(request,nome,id):  
    msg="A enviar email a "+nome+" a informar que o seu registo foi rejeitado"
    return render(request=request,
                  template_name="utilizadores/enviar_email_rejeitar.html",
                  context={"msg": msg, "id":id})

def alterar_utilizador_admin(request,id):

    if request.user.is_authenticated:    
        utilizador_atual = get_user(request)
        if utilizador_atual.groups.filter(name = "Administrador").exists():
            u = "Administrador"         
        else:
            return redirect('utilizadores:mensagem',5) 
    else:
        return redirect('utilizadores:mensagem',5)


    
    user = User.objects.get(id=id)
    if user.groups.filter(name = "Coordenador").exists():
        tipo=3            
        u = "Coordenador"
        utilizador_object = Coordenador.objects.get(id=user.id)
        utilizador_form = CoordenadorAlterarPerfilForm(instance=utilizador_object)
        perfil= "Coordenador"
    elif user.groups.filter(name = "Administrador").exists():
        tipo=5
        u = "Administrador"
        utilizador_object = Administrador.objects.get(id=user.id)
        utilizador_form = AdministradorAlterarPerfilForm(instance=utilizador_object)
        perfil="Administrador"
    elif user.groups.filter(name = "ProfessorUniversitario").exists():
        tipo=2
        u = "ProfessorUniversitario"
        utilizador_object = ProfessorUniversitario.objects.get(id=user.id)
        utilizador_form = ProfessorUniversitarioAlterarPerfilForm(instance=utilizador_object)
        perfil="Professor Universitario"
    elif user.groups.filter(name = "Colaborador").exists():
        tipo=4            
        u = "Colaborador"
        utilizador_object = Colaborador.objects.get(id=user.id)
        utilizador_form = ColaboradorAlterarPerfilForm(instance=utilizador_object)
        perfil= "Colaborador"
    elif user.groups.filter(name = "Participante").exists():
        tipo=1
        u = "Participante" 
        utilizador_object = Participante.objects.get(id=user.id)
        utilizador_form = ParticipanteAlterarPerfilForm(instance=utilizador_object)
        perfil= "Participante"
    else:
        return redirect('utilizadores:mensagem',5)     



    msg=False
    if request.method == "POST":
        submitted_data = request.POST.copy()
        if tipo == 1:
            form = ParticipanteAlterarPerfilForm(submitted_data,instance=utilizador_object)
            my_group = Group.objects.get(name='Participante') 
        elif tipo == 2:
            form = ProfessorUniversitarioAlterarPerfilForm(submitted_data,instance=utilizador_object)
            my_group = Group.objects.get(name='ProfessorUniversitario')
        elif tipo == 3:
            form = CoordenadorAlterarPerfilForm(submitted_data,instance=utilizador_object)
            my_group = Group.objects.get(name='Coordenador')
        elif tipo == 4:
            form = ColaboradorAlterarPerfilForm(submitted_data,instance=utilizador_object)
            my_group = Group.objects.get(name='Colaborador')
        elif tipo == 5:
            form = AdministradorAlterarPerfilForm(submitted_data,instance=utilizador_object)
            my_group = Group.objects.get(name='Administrador')    
        else:
             return redirect('utilizadores:mensagem',5)   

        email = request.POST.get('email')

        erros=[]


        if email and User.objects.exclude(email=utilizador_object.email).filter(email=email).exists():
            erros.append('O email já existe')
        elif email==None:
            erros.append('O email é inválido')

        if form.is_valid() and len(erros)==0:
            utilizador_form_object = form.save(commit=False)
            if tipo==2 or tipo==3 or tipo==4:
                utilizador_form_object.faculdade = Unidadeorganica.objects.get(id=submitted_data['faculdade'])
                utilizador_form_object.departamento = Departamento.objects.get(id=submitted_data['departamento'])
            utilizador_form_object.save()  
            return redirect('utilizadores:consultar-utilizadores') 
        else:
            msg=True
            return render(request=request,
                          template_name="utilizadores/alterar_utilizador_admin.html",
                          context={"form": form, 'perfil': perfil, 'u': u,'registo' : tipo,'msg': msg, 'erros':erros})
    else:

        return render(request=request,
                  template_name="utilizadores/alterar_utilizador_admin.html",
                  context={"form": utilizador_form, 'perfil': perfil,'u': u,'registo' : tipo,'msg': msg})



def alterar_utilizador(request):
    if request.user.is_authenticated:    
        user = get_user(request)
        if user.groups.filter(name = "Coordenador").exists():
            tipo=3            
            u = "Coordenador"
            utilizador_object = Coordenador.objects.get(id=user.id)
            utilizador_form = CoordenadorAlterarPerfilForm(instance=utilizador_object)
            perfil= "Coordenador"
        elif user.groups.filter(name = "Administrador").exists():
            tipo=5
            u = "Administrador"
            utilizador_object = Administrador.objects.get(id=user.id)
            utilizador_form = AdministradorAlterarPerfilForm(instance=utilizador_object)
            perfil="Administrador"
        elif user.groups.filter(name = "ProfessorUniversitario").exists():
            tipo=2
            u = "ProfessorUniversitario"
            utilizador_object = ProfessorUniversitario.objects.get(id=user.id)
            utilizador_form = ProfessorUniversitarioAlterarPerfilForm(instance=utilizador_object)
            perfil="Professor Universitario"
        elif user.groups.filter(name = "Colaborador").exists():
            tipo=4            
            u = "Colaborador"
            utilizador_object = Colaborador.objects.get(id=user.id)
            utilizador_form = ColaboradorAlterarPerfilForm(instance=utilizador_object)
            perfil= "Colaborador"
        elif user.groups.filter(name = "Participante").exists():
            tipo=1
            u = "Participante" 
            utilizador_object = Participante.objects.get(id=user.id)
            utilizador_form = ParticipanteAlterarPerfilForm(instance=utilizador_object)
            perfil= "Participante"
        else:
            return redirect('utilizadores:mensagem',5)     
    else:
        return redirect('utilizadores:mensagem',5) 


    msg=False
    if request.method == "POST":
        submitted_data = request.POST.copy()
        if tipo == 1:
            form = ParticipanteAlterarPerfilForm(submitted_data,instance=utilizador_object)
            my_group = Group.objects.get(name='Participante') 
        elif tipo == 2:
            form = ProfessorUniversitarioAlterarPerfilForm(submitted_data,instance=utilizador_object)
            my_group = Group.objects.get(name='ProfessorUniversitario')
        elif tipo == 3:
            form = CoordenadorAlterarPerfilForm(submitted_data,instance=utilizador_object)
            my_group = Group.objects.get(name='Coordenador')
        elif tipo == 4:
            form = ColaboradorAlterarPerfilForm(submitted_data,instance=utilizador_object)
            my_group = Group.objects.get(name='Colaborador')
        elif tipo == 5:
            form = AdministradorAlterarPerfilForm(submitted_data,instance=utilizador_object)
            my_group = Group.objects.get(name='Administrador')    
        else:
            return redirect('utilizadores:mensagem',5) 

        username = request.POST.get('newusername')
        email = request.POST.get('email')

        erros=[]
        if username and User.objects.exclude(username=utilizador_object.username).filter(username=username).exists():
            erros.append('O username já existe')
        elif username=="":
            erros.append('Todos os campos são obrigatórios!')

        if email and User.objects.exclude(email=utilizador_object.email).filter(email=email).exists():
            erros.append('O email já existe')
        elif email==None:
            erros.append('O email é inválido')

        if form.is_valid() and len(erros)==0:
            utilizador_form_object = form.save(commit=False)
            utilizador_form_object.username = username
            if tipo==2 or tipo==3 or tipo==4:
                utilizador_form_object.faculdade = Unidadeorganica.objects.get(id=submitted_data['faculdade'])
                utilizador_form_object.departamento = Departamento.objects.get(id=submitted_data['departamento'])
            if tipo==1 or tipo==5:
                utilizador_form_object.valido="True"
            else:
                utilizador_form_object.valido="False"    
            utilizador_form_object.save()  
            return redirect('utilizadores:mensagem',8) 
        else:
            msg=True
            return render(request=request,
                          template_name="utilizadores/alterar_utilizador.html",
                          context={"form": form, 'perfil': perfil, 'u': u,'registo' : tipo,'msg': msg,'username':username, 'erros':erros})
    else:

        return render(request=request,
                  template_name="utilizadores/alterar_utilizador.html",
                  context={"form": utilizador_form, 'perfil': perfil,'u': u,'registo' : tipo,'username':user.username,'msg': msg})


def home(request):
    if request.user.is_authenticated:    
        user = get_user(request)
        if user.groups.filter(name = "Coordenador").exists():
            u = "Coordenador"
        elif user.groups.filter(name = "Administrador").exists():
            u = "Administrador"
        elif user.groups.filter(name = "ProfessorUniversitario").exists():
            u = "ProfessorUniversitario"
        elif user.groups.filter(name = "Colaborador").exists():
            u = "Colaborador"
        elif user.groups.filter(name = "Participante").exists():
            u = "Participante" 
        else:
            u=""     
    else:
        u=""
    
    return render(request, "utilizadores/inicio.html",context={ 'u': u})


def concluir_registo(request,id):
    if request.user.is_authenticated:    
        user = get_user(request)
        if user.groups.filter(name = "Coordenador").exists():
            u = "Coordenador"
        elif user.groups.filter(name = "Administrador").exists():
            u = "Administrador"
        elif user.groups.filter(name = "ProfessorUniversitario").exists():
            u = "ProfessorUniversitario"
        elif user.groups.filter(name = "Colaborador").exists():
            u = "Colaborador"
        elif user.groups.filter(name = "Participante").exists():
            u = "Participante" 
        else:
            u=""   
    else:
        u=""
    if id==1:
        participante=True
    else:
        participante=False
    return render(request=request,
                  template_name="utilizadores/concluir_registo.html",
                  context={'participante': participante, 'u': u})


def mensagem(request, id):
    if request.user.is_authenticated:    
        user = get_user(request)
        if user.groups.filter(name = "Coordenador").exists():
            u = "Coordenador"
        elif user.groups.filter(name = "Administrador").exists():
            u = "Administrador"
        elif user.groups.filter(name = "ProfessorUniversitario").exists():
            u = "ProfessorUniversitario"
        elif user.groups.filter(name = "Colaborador").exists():
            u = "Colaborador"
        elif user.groups.filter(name = "Participante").exists():
            u = "Participante" 
        else:
            u=""     
    else:
        u=""


    if id == 1:
        user = get_user(request)
        m = "Bem vindo(a) "+user.first_name
        tipo = "info"

    elif id == 2:
        m = "Até á próxima!"
        tipo = "info"

    elif id == 3:
        m = "Registo feito com sucesso!"
        tipo = "sucess"

    elif id == 4:
        m = "É necessário fazer login primeiro"
        tipo = "error"

    elif id == 5:
        m = "Não permitido"
        tipo = "error"
    elif id == 6:
        m = "Senha alterada com sucesso!"
        tipo = "success"    
    elif id == 7:
        m = "Conta apagada com sucesso"
        tipo = "success"  
    elif id == 8:
        m = "Perfil alterado com sucesso"
        tipo = "success"
    elif id == 9:
        m = "O seu registo ainda não foi validado, por favor aguarde o email de confirmação"
        tipo = "info" 
    elif id == 10:
        m = "O seu registo não é válido"
        tipo = "error"                         
    else:
        return redirect('utilizadores:login')
 
    return render(request=request,
        template_name="utilizadores/mensagem.html", context={'m': m, 'tipo': tipo ,'u': u})
