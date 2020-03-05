### Pre-requisitos

* [Python 3.8.2](https://www.python.org/downloads/)
* [Git](https://git-scm.com/downloads)

### Instalação

1. Abrir o terminal na pasta onde vai ser guardado o projeto

e.g.:
```SH
cd ~/Documentos/Universidade/LES
```

2. Clonar o projeto do github

```SH
git clone https://github.com/tiagonuneslx/dia-aberto.git
```

3. Entrar na pasta do projeto

```SH
cd dia-aberto
```

4. Criar o ambiente do projeto (venv)

**Atenção: A versão de Python com a qual criar o ambiente do projeto deve ser igual para todos (v3.8.2)**

Para verificar se a versão de Python instalada é a indicada:

Linux:
```SH
python3.8 -V
```

Windows:
```SH
python -V
```

Se o comando anterior não devolver `Python 3.8.2`, há que mudar a versão antes de criar o ambiente.

Se a versão do Python estiver correta, segue a criação do ambiente (na pasta do projeto):

Linux:
```SH
python3.8 -m venv env
```

Windows:
```SH
python -m venv env
```

5. Ativar o ambiente no terminal

Linux:
```SH
source env/bin/activate
```

Windows:
```SH
env\scripts\activate
```

A extensão padrão de Python do VSCode tem a opção de ativar automaticamente o ambiente em novos terminais. Para ativar a funcionalidade, há que abrir a **Palete de Comandos (F1)**,  **Python: Selecionar Interpretador** e escolher a opção cuja localização comece com `./env` ou `.\env`.

6. Atualizar as dependências iniciais do ambiente

```SH
pip install --upgrade pip setuptools
```

7. Instalar as dependências do projeto

```SH
pip install -r requirements.txt
```

## Comandos fundamentais

#### Ativar o ambiente virtual no terminal

Linux:
```SH
source env/bin/activate
```

Windows:
```SH
env\scripts\activate
```

#### Iniciar o servidor localmente

```SH
python manage.py runserver
```

#### Gerar migrações automaticamente através dos modelos

```SH
python manage.py makemigrations
```

#### Aplicar as migrações à base de dados

```SH
python manage.py migrate
```

#### Instalar nova dependência

```SH
pip install [dependência] && pip freeze > requirements.txt
```

## Dependências

* pip - Gestor de Pacotes (Python)
* setuptools - Ferramentas (Python)
* Django - Web Framework
* sqlparse - (Django)
* pytz - (Django)
* asgiref - (Django)