mkdir -p static
mkdir -p staticfiles_build/static
# mkdir -p main/static
pip install -r requirements.txt
# python3.9 manage.py makemigrations 
python3.9 manage.py migrate 
#python3.9 manage.py collectstatic --noinput