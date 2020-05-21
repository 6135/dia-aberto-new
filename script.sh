find . -path "*/migrations/*.py" ! -path "./env/*" ! -name "__init__.py" -delete
find . -path "*/migrations/*.pyc" ! -path "./env/*" -delete