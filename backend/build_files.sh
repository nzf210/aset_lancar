mkdir -p staticfiles_build/static
mkdir -p static
touch main/db.sqlite3
pip install -r requirements.txt
# python3.9 manage.py makemigrations
# python3.9 manage.py migrate
python3.9 main/manage.py collectstatic --noinput