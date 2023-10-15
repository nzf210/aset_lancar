pip install -r requirements.txt
# python3.9 manage.py makemigrations
# python3.9 manage.py migrate
python3.9 main/manage.py collectstatic --noinput
python3.9 main/manage.py findstatic
# python3.9 manage.py runserver 0.0.0.0:8000