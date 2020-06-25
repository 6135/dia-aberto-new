for file in fixtures/*; do
    python manage.py loaddata $file
done