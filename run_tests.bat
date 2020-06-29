:: Componente Utilizadores

python manage.py test utilizadores.tests.funcionais.test_login_ok
python manage.py test utilizadores.tests.funcionais.test_login_nao_existe
python manage.py test utilizadores.tests.funcionais.test_login_pass_errada
python manage.py test utilizadores.tests.funcionais.test_logout
python manage.py test utilizadores.tests.funcionais.test_alterar_pass_ok
python manage.py test utilizadores.tests.funcionais.test_alterar_pass_erro
python manage.py test utilizadores.tests.funcionais.test_criar_participante_ok
python manage.py test utilizadores.tests.funcionais.test_criar_participante_erro
python manage.py test utilizadores.tests.funcionais.test_criar_prof_universitario_ok
python manage.py test utilizadores.tests.funcionais.test_criar_prof_universitario_erro
python manage.py test utilizadores.tests.funcionais.test_criar_coordenador_ok
python manage.py test utilizadores.tests.funcionais.test_criar_coordenador_erro
python manage.py test utilizadores.tests.funcionais.test_criar_colaborador_ok
python manage.py test utilizadores.tests.funcionais.test_criar_colaborador_erro
python manage.py test utilizadores.tests.funcionais.test_criar_administrador_ok
python manage.py test utilizadores.tests.funcionais.test_criar_administrador_erro
python manage.py test utilizadores.tests.funcionais.test_apagar_participante
python manage.py test utilizadores.tests.funcionais.test_apagar_prof_universitario
python manage.py test utilizadores.tests.funcionais.test_apagar_coordenador
python manage.py test utilizadores.tests.funcionais.test_apagar_colaborador
python manage.py test utilizadores.tests.funcionais.test_apagar_administrador
python manage.py test utilizadores.tests.funcionais.test_alterar_participante_ok
python manage.py test utilizadores.tests.funcionais.test_alterar_participante_erro
python manage.py test utilizadores.tests.funcionais.test_alterar_prof_universitario_ok
python manage.py test utilizadores.tests.funcionais.test_alterar_prof_universitario_erro
python manage.py test utilizadores.tests.funcionais.test_alterar_coordenador_ok
python manage.py test utilizadores.tests.funcionais.test_alterar_coordenador_erro
python manage.py test utilizadores.tests.funcionais.test_alterar_colaborador_ok
python manage.py test utilizadores.tests.funcionais.test_alterar_colaborador_erro
python manage.py test utilizadores.tests.funcionais.test_alterar_administrador_ok
python manage.py test utilizadores.tests.funcionais.test_alterar_administrador_erro
python manage.py test utilizadores.tests.funcionais.test_consultar_utilizadores
python manage.py test utilizadores.tests.funcionais.test_alterar_perfil_participante_ok
python manage.py test utilizadores.tests.funcionais.test_alterar_perfil_participante_erro
python manage.py test utilizadores.tests.funcionais.test_alterar_perfil_prof_universitario_ok
python manage.py test utilizadores.tests.funcionais.test_alterar_perfil_prof_universitario_erro
python manage.py test utilizadores.tests.funcionais.test_alterar_perfil_coordenador_ok
python manage.py test utilizadores.tests.funcionais.test_alterar_perfil_coordenador_erro
python manage.py test utilizadores.tests.funcionais.test_alterar_perfil_colaborador_ok
python manage.py test utilizadores.tests.funcionais.test_alterar_perfil_colaborador_erro
python manage.py test utilizadores.tests.funcionais.test_alterar_perfil_administrador_ok
python manage.py test utilizadores.tests.funcionais.test_alterar_perfil_administrador_erro
python manage.py test utilizadores.tests.funcionais.test_apagar_conta
python manage.py test utilizadores.tests.funcionais.test_rejeitar_utilizador
python manage.py test utilizadores.tests.funcionais.test_validar_utilizador


:: Componente Colaboradores

python manage.py test colaboradores.tests.funcionais.test_consultar_tarefas


:: Componente Notificacoes

python manage.py test notificacoes.tests.funcionais.test_enviar_mensagem_participante_individual
python manage.py test notificacoes.tests.funcionais.test_enviar_mensagem_unidade_organica_individual
python manage.py test notificacoes.tests.funcionais.test_enviar_mensagem_admin_individual
python manage.py test notificacoes.tests.funcionais.test_enviar_mensagem_participante_grupo
python manage.py test notificacoes.tests.funcionais.test_enviar_mensagem_unidade_organica_grupo
python manage.py test notificacoes.tests.funcionais.test_enviar_mensagem_admin_grupo
python manage.py test notificacoes.tests.funcionais.test_receber_mensagem