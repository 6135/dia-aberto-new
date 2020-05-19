find . -path "*/migrations/*.py" ! -path "./env/*" ! -name "__init__.py" -delete
find . -path "*/migrations/*.pyc" ! -path "./env/*" -delete
mysql -p < custom-scripts/linux/reset-database.sql
python manage.py makemigrations
python manage.py migrate
custom-scripts/linux/load-fixtures.sh