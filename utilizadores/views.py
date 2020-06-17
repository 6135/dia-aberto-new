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
from notificacoes import views

# Verifica se o utilizador que esta logado pertence a pelo menos um dos perfeis mencionados e.g. user_profile = {Administrador,Coordenador,ProfessorUniversitario}
# Isto faz com que o user que esta logado possa ser qualquer um dos 3 perfeis.

def user_check(request, user_profile = None):
    if not request.user.is_authenticated:
        return {'exists': False, 'render': redirect('utilizadores:login')}
    elif user_profile is not None:
        matches_profile = False
        for profile in user_profile:
            if profile.objects.filter(utilizador_ptr_id = request.user.id).exists():
                return {'exists': True, 'firstProfile': profile.objects.filter(utilizador_ptr_id = request.user.id).first()}
        return {'exists': False, 
                'render': render(request=request,
                            template_name='mensagem.html',
                            context={
                                'tipo':'error',
                                'm':'Não tem permissões para aceder a esta pagina!'
                            })
                }
    return {'exists': False, 'render': render()}


# Carregar todos os departamentos para uma determinada faculdade 

def load_departamentos(request):
    faculdadeid = request.GET.get('faculdade')
    departamentos = Departamento.objects.filter(unidadeorganicaid=faculdadeid).order_by('nome')
    return render(request, 'utilizadores/departamento_dropdown_list_options.html', {'departamentos': departamentos})



# Carregar todos os cursos para uma determinada faculdade 

def load_cursos(request):
    faculdadeid = request.GET.get('faculdade')
    cursos = Curso.objects.filter(unidadeorganicaid=faculdadeid).order_by('nome')
    return render(request, 'utilizadores/curso_dropdown_list_options.html', {'cursos': cursos})



# Consultar todos os utilizadores com as funcionalidades dos filtros 

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



# Escolher tipo de perfil para criar um utilizador

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
                    "Professor Universitário", "Coordenador", "Colaborador","Administrador"]
    return render(request=request, template_name='utilizadores/escolher_perfil.html', context={"utilizadores": utilizadores,'u': u})




# Criar um novo utilizador que poderá ter de ser validado dependendo do seu tipo

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
                if tipo == 2 or tipo == 3 or tipo == 4: #Enviar Notificacao Automatica !!!!!!!!!
                    recipient_id = user.departamento.id #Enviar Notificacao Automatica !!!!!!!!!
                else: #Enviar Notificacao Automatica !!!!!!!!!
                    recipient_id = -1 #Enviar Notificacao Automatica !!!!!!!!!
                views.enviar_notificacao_automatica(request,"validarRegistosPendentes",recipient_id) #Enviar Notificacao Automatica !!!!!!!!!
                user.save()
                p=0

            if request.user.is_authenticated:    
                user = get_user(request)
                if user.groups.filter(name = "Coordenador").exists():
                    return redirect('utilizadores:mensagem',9)  
                elif user.groups.filter(name = "Administrador").exists():
                    return redirect('utilizadores:mensagem',9)  
            else:   
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
            form = AdministradorRegisterForm()
            perfil = "Administrador" 
        else:
            return redirect("utilizadores:escolher-perfil")
    return render(request=request,
                  template_name="utilizadores/criar_utilizador.html",
                  context={"form": form, 'perfil': perfil,'u': u,'registo' : tipo,'msg': msg})


# Fazer login na plataforma do dia aberto e gestão de acessos à plataforma

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
                    msg=True
                    error="O seu registo ainda não foi validado"
                elif utilizador.valido=="Rejeitado":
                    msg=True
                    error="O seu registo não é válido"
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




# Fazer logout na plataforma

def logout_action(request):
    logout(request)
    return redirect('utilizadores:mensagem',2)



# Alterar a password do utilizador

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




# Funcionalidade de rejeitar um utilizador na pagina de consultar utilizadores

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



# Alterar o idioma da plataforma

def alterar_idioma(request):   
     return redirect('utilizadores:mensagem',5)  


#Validar um utilizador na pagina consultar utilizadores

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



#Apagar um utilizador na pagina consultar utilizadores

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

    print(u)
    u.delete() 
    return redirect('utilizadores:consultar-utilizadores')   


#Apagar a propria conta 

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


#Envio de email quando o utilizador é validado na pagina consultar utilizadores

def enviar_email_validar(request,nome,id):  
    msg="A enviar email a "+nome+" a informar que o seu registo foi validado"
    return render(request=request,
                  template_name="utilizadores/enviar_email_validar.html",
                  context={"msg": msg, "id":id})

#Envio de email quando o utilizador é rejeitado na pagina consultar utilizadores

def enviar_email_rejeitar(request,nome,id):  
    msg="A enviar email a "+nome+" a informar que o seu registo foi rejeitado"
    return render(request=request,
                  template_name="utilizadores/enviar_email_rejeitar.html",
                  context={"msg": msg, "id":id})

#Funcionalidade de o administrador alterar um utilizador

def alterar_utilizador_admin(request,id):

    if request.user.is_authenticated:    
        utilizador_atual = get_user(request)
        if utilizador_atual.groups.filter(name = "Administrador").exists():
            admin = "Administrador"         
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
                          context={"form": form, 'perfil': perfil, 'u': admin,'registo' : tipo,'msg': msg, 'erros':erros,'id':id})
    else:

        return render(request=request,
                  template_name="utilizadores/alterar_utilizador_admin.html",
                  context={"form": utilizador_form, 'perfil': perfil,'u': admin,'registo' : tipo,'msg': msg,'id':id})


#Funcionalidade de alterar dados de conta

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


#Pagina principal da plataforma

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
    
    return render(request, "inicio.html",context={ 'u': u})

#Pagina que é mostrada ao utilizador quando faz um registo na plataforma

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


#Template de mensagens informativas/erro/sucesso

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
        m = "Perfil criado com sucesso"
        tipo = "success"                         
    else:
        return redirect('utilizadores:login')
 
    return render(request=request,
        template_name="utilizadores/mensagem.html", context={'m': m, 'tipo': tipo ,'u': u})



# Funcionalidade de o administrador alterar o perfil de um dado utilizador 
# Redireciona para uma pagina onde é possivel escolher o perfil que quer alterar

def mudar_perfil_escolha_admin(request,id):
    if request.user.is_authenticated:    
        user = get_user(request)
        if user.groups.filter(name = "Administrador").exists():
            u = "Administrador"
        else:
            return redirect('utilizadores:mensagem',5)   
    else:
        return redirect('utilizadores:mensagem',5) 

    user=User.objects.get(id=id)  
    if user.groups.filter(name = "Coordenador").exists():           
        x = "Coordenador"
    elif user.groups.filter(name = "Administrador").exists():
        x = "Administrador"
    elif user.groups.filter(name = "ProfessorUniversitario").exists():
        x = "Professor Universitário"
    elif user.groups.filter(name = "Colaborador").exists():        
        x = "Colaborador"
    elif user.groups.filter(name = "Participante").exists():
        x = "Participante" 
    else:
        return redirect('utilizadores:mensagem',5)     

    utilizadores = ["Participante",
                    "Professor Universitário", "Coordenador", "Colaborador","Administrador"]
    return render(request=request, template_name='utilizadores/mudar_perfil_escolha_admin.html', context={"utilizadores": utilizadores,'u': u,'id':id ,'x':x})


# Funcionalidade de o utilizador alterar o seu proprio perfil
# Redireciona para uma pagina onde é possivel escolher o perfil que quer alterar

def mudar_perfil_escolha(request):
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

    user=User.objects.get(id=user.id)  
    
    if user.groups.filter(name = "Coordenador").exists():           
        x = "Coordenador"
    elif user.groups.filter(name = "Administrador").exists():
        x = "Administrador"
    elif user.groups.filter(name = "ProfessorUniversitario").exists():
        x = "ProfessorUniversitario"
    elif user.groups.filter(name = "Colaborador").exists():        
        x = "Colaborador"
    elif user.groups.filter(name = "Participante").exists():
        x = "Participante" 
    else:
        return redirect('utilizadores:mensagem',5)     

    utilizadores = ["Participante",
                    "Professor Universitário", "Coordenador", "Colaborador","Administrador"]
    return render(request=request, template_name='utilizadores/mudar_perfil_escolha.html', context={"utilizadores": utilizadores,'u': u,'id':id ,'x':x})




# Funcionalidade de o administrador alterar o perfil de um dado utilizador 
# Redireciona para uma pagina que contem os dados já existentes do utilizador a alterar sendo que apenas os campos diferentes não estão preenchidos

def mudar_perfil_admin(request,tipo,id):
    if request.user.is_authenticated:    
        user = get_user(request)
        if user.groups.filter(name = "Administrador").exists():
            u = "Administrador"
        else:
            return redirect('utilizadores:mensagem',5)   
    else:
        return redirect('utilizadores:mensagem',5) 

    if tipo == 1:
        form = ParticipanteAlterarPerfilForm()
        perfil = "Participante"
    elif tipo == 2:
        form = ProfessorUniversitarioAlterarPerfilForm()
        perfil = "Professor Universitario"
    elif tipo == 3:
        form = CoordenadorAlterarPerfilForm()
        perfil = "Coordenador"
    elif tipo == 4:
        form = ColaboradorAlterarPerfilForm()
        perfil = "Colaborador"
    elif tipo == 5:
        form = AdministradorAlterarPerfilForm()
        perfil = "Administrador" 
    else:
        return redirect('utilizadores:mensagem',5) 

    user=User.objects.get(id=id)
    if user.groups.filter(name = "Coordenador").exists():         
        utilizador_object = Coordenador.objects.get(id=user.id)
        gabinete=utilizador_object.gabinete
        if tipo!=1 and tipo!=5:
            form.fields['departamento'].initial =utilizador_object.departamento.id
            form.fields['faculdade'].initial =utilizador_object.faculdade.id

    elif user.groups.filter(name = "Administrador").exists():
        utilizador_object = Administrador.objects.get(id=user.id)
        gabinete=utilizador_object.gabinete
    elif user.groups.filter(name = "ProfessorUniversitario").exists():
        utilizador_object = ProfessorUniversitario.objects.get(id=user.id)
        gabinete=utilizador_object.gabinete
        if tipo!=1 and tipo!=5:
            form.fields['departamento'].initial =utilizador_object.departamento.id
            form.fields['faculdade'].initial =utilizador_object.faculdade.id
    elif user.groups.filter(name = "Colaborador").exists():
        utilizador_object = Colaborador.objects.get(id=user.id) 
        gabinete=""
        if tipo!=1 and tipo!=5:
            form.fields['departamento'].initial =utilizador_object.departamento.id
            form.fields['faculdade'].initial = utilizador_object.faculdade.id
    elif user.groups.filter(name = "Participante").exists():
        utilizador_object = Participante.objects.get(id=user.id)  
        gabinete=""   
    else:
        return redirect('utilizadores:mensagem',5) 
    msg=False
    if request.method == "POST":
        submitted_data = request.POST
        if tipo == 1:
            form = ParticipanteAlterarPerfilForm(submitted_data)
            my_group = Group.objects.get(name='Participante')
        elif tipo == 2:
            form = ProfessorUniversitarioAlterarPerfilForm(submitted_data)
            my_group = Group.objects.get(name='ProfessorUniversitario')
        elif tipo == 3:
            form = CoordenadorAlterarPerfilForm(submitted_data)
            my_group = Group.objects.get(name='Coordenador')
        elif tipo == 4:
            form = ColaboradorAlterarPerfilForm(submitted_data)
            my_group = Group.objects.get(name='Colaborador')
        elif tipo == 5:
            form = AdministradorAlterarPerfilForm(submitted_data)
            my_group = Group.objects.get(name='Administrador')  
        else:
            return redirect('utilizadores:mensagem',5) 

        username = request.POST.get('username')
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

            
            utilizador_form_object.valido=utilizador_object.valido
            utilizador_object.delete()
            utilizador_form_object.password=utilizador_object.password
            utilizador_form_object.id=id
            utilizador_form_object.save()  
            my_group.user_set.add(utilizador_form_object)
            
            return redirect('utilizadores:mensagem',8) 
        else:
            msg=True
            return render(request=request,
                          template_name="utilizadores/mudar_perfil_admin.html",
                          context={"form": form, 'perfil': perfil, 'u': u,'user':utilizador_object,'registo' : tipo,'msg': msg, 'erros':erros,'gabinete':gabinete,'username':username})
    else:
        username=utilizador_object.username
        return render(request=request,
                  template_name="utilizadores/mudar_perfil_admin.html",
                  context={"form": form, 'perfil': perfil,'u': u,'registo' : tipo,'user':utilizador_object,'msg': msg,'gabinete':gabinete,'username':username})



# Alterar perfil do proprio utilizador
# Redireciona para uma pagina que contem os dados já existentes do utilizador a alterar sendo que apenas os campos diferentes não estão preenchidos


def mudar_perfil(request,tipo):       
    if request.user.is_authenticated:    
        user = get_user(request)
        id=user.id
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

    if tipo == 1:
        form = ParticipanteAlterarPerfilForm()
        perfil = "Participante"
    elif tipo == 2:
        form = ProfessorUniversitarioAlterarPerfilForm()
        perfil = "Professor Universitario"
    elif tipo == 3:
        form = CoordenadorAlterarPerfilForm()
        perfil = "Coordenador"
    elif tipo == 4:
        form = ColaboradorAlterarPerfilForm()
        perfil = "Colaborador"
    elif tipo == 5:
        form = AdministradorAlterarPerfilForm()
        perfil = "Administrador" 
    else:
        return redirect('utilizadores:mensagem',5) 

    user=User.objects.get(id=user.id)
    if user.groups.filter(name = "Coordenador").exists():         
        utilizador_object = Coordenador.objects.get(id=user.id)
        gabinete=utilizador_object.gabinete
        if tipo!=1 and tipo!=5:
            form.fields['departamento'].initial =utilizador_object.departamento.id
            form.fields['faculdade'].initial =utilizador_object.faculdade.id

    elif user.groups.filter(name = "Administrador").exists():
        utilizador_object = Administrador.objects.get(id=user.id)
        gabinete=utilizador_object.gabinete
    elif user.groups.filter(name = "ProfessorUniversitario").exists():
        utilizador_object = ProfessorUniversitario.objects.get(id=user.id)
        gabinete=utilizador_object.gabinete
        if tipo!=1 and tipo!=5:
            form.fields['departamento'].initial =utilizador_object.departamento.id
            form.fields['faculdade'].initial =utilizador_object.faculdade.id
    elif user.groups.filter(name = "Colaborador").exists():
        utilizador_object = Colaborador.objects.get(id=user.id) 
        gabinete=""
        if tipo!=1 and tipo!=5:
            form.fields['departamento'].initial =utilizador_object.departamento.id
            form.fields['faculdade'].initial = utilizador_object.faculdade.id
    elif user.groups.filter(name = "Participante").exists():
        utilizador_object = Participante.objects.get(id=user.id)  
        gabinete=""   
    else:
        return redirect('utilizadores:mensagem',5) 
    msg=False
    if request.method == "POST":
        submitted_data = request.POST
        if tipo == 1:
            form = ParticipanteAlterarPerfilForm(submitted_data)
            my_group = Group.objects.get(name='Participante')
        elif tipo == 2:
            form = ProfessorUniversitarioAlterarPerfilForm(submitted_data)
            my_group = Group.objects.get(name='ProfessorUniversitario')
        elif tipo == 3:
            form = CoordenadorAlterarPerfilForm(submitted_data)
            my_group = Group.objects.get(name='Coordenador')
        elif tipo == 4:
            form = ColaboradorAlterarPerfilForm(submitted_data)
            my_group = Group.objects.get(name='Colaborador')
        elif tipo == 5:
            form = AdministradorAlterarPerfilForm(submitted_data)
            my_group = Group.objects.get(name='Administrador')  
        else:
            return redirect('utilizadores:mensagem',5) 

        username = request.POST.get('username')
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

            
            utilizador_form_object.valido=utilizador_object.valido
            utilizador_form_object.password=utilizador_object.password
            utilizador_object.delete()
            utilizador_form_object.id=id
            utilizador_form_object.save()  
            my_group.user_set.add(utilizador_form_object)

            if tipo == 2 or tipo == 3 or tipo == 4 or tipo == 5: #Enviar Notificacao Automatica !!!!!!!!!
                if tipo == 2 or tipo == 3 or tipo == 4: #Enviar Notificacao Automatica !!!!!!!!!
                    recipient_id = utilizador_form_object.departamento.id #Enviar Notificacao Automatica !!!!!!!!!
                else: #Enviar Notificacao Automatica !!!!!!!!!
                    recipient_id = -1 #Enviar Notificacao Automatica !!!!!!!!!
                views.enviar_notificacao_automatica(request,"validarAlteracoesPerfil",recipient_id) #Enviar Notificacao Automatica !!!!!!!!!
            return redirect('utilizadores:logout') 
        else:
            msg=True
            return render(request=request,
                          template_name="utilizadores/mudar_perfil.html",
                          context={"form": form, 'perfil': perfil, 'u': u,'user':utilizador_object,'registo' : tipo,'msg': msg, 'erros':erros,'gabinete':gabinete,'username':username})
    else:
        username=utilizador_object.username
        return render(request=request,
                  template_name="utilizadores/mudar_perfil.html",
                  context={"form": form, 'perfil': perfil,'u': u,'registo' : tipo,'user':utilizador_object,'msg': msg,'gabinete':gabinete,'username':username})

