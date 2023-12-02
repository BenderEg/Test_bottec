python manage.py migrate
python manage.py collectstatic
python manage.py createsuperuser --username Egor --noinput
uwsgi --ini uwsgi.ini