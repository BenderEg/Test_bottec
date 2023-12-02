python manage.py migrate
python manage.py collectstatic
python manage.py createsuperuser --noinput
uwsgi --ini uwsgi.ini