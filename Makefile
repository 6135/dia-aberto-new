setup:
		python3 -m venv ~/.dia-aberto-new/
		source ~/.dia-aberto.new/bin/activate
install:
		pip3 install --upgrade pip
		pip3 install -r requirements.txt
		python3 manage.py makemigrations
		python3 manage.py migrate
		python3 manage.py create_groups
		python3 manage.py create_admin test_user
lint: 
		#hadolint Dockerfile #uncomment to explore linting Dockerfiles
		pylint --disable=R,C configuracao/*.py
format:
		black *.py
test:
		python3 manage.py test utilizadores.tests.funcionais.test_login_ok
		python3 manage.py test utilizadores.tests.funcionais.test_login_nao_existe
		python3 manage.py test utilizadores.tests.funcionais.test_login_pass_errada
		python3 manage.py test utilizadores.tests.funcionais.test_logout
		python3 manage.py test utilizadores.tests.funcionais.test_alterar_pass_ok
		python3 manage.py test utilizadores.tests.funcionais.test_alterar_pass_erro
		python3 manage.py test utilizadores.tests.funcionais.test_criar_utilizador_ok
		python3 manage.py test utilizadores.tests.funcionais.test_criar_utilizador_erro
		python3 manage.py test utilizadores.tests.funcionais.test_alterar_utilizador_ok
		python3 manage.py test utilizadores.tests.funcionais.test_alterar_utilizador_erro
		python3 manage.py test utilizadores.tests.funcionais.test_consultar_utilizadores
		python3 manage.py test utilizadores.tests.funcionais.test_rejeitar_utilizador
		python3 manage.py test utilizadores.tests.funcionais.test_validar_utilizador
		
		#Componente Colaboradores
		
		python3 manage.py test colaboradores.tests.funcionais.test_consultar_tarefas
		
		#Componente Notificacoes
		
		python3 manage.py test notificacoes.tests.funcionais.test_enviar_mensagem_individual
		python3 manage.py test notificacoes.tests.funcionais.test_enviar_mensagem_participante_grupo
		python3 manage.py test notificacoes.tests.funcionais.test_enviar_mensagem_unidade_organica_grupo
		python3 manage.py test notificacoes.tests.funcionais.test_enviar_mensagem_admin_grupo
		python3 manage.py test notificacoes.tests.funcionais.test_receber_mensagem

all: install format lint test