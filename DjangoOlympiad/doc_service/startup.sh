# Откат миграций с подтверждением
python manage.py migrate api zero --fake 

# Создание миграций для всех приложений
python manage.py makemigrations

# Применение всех миграций
python manage.py migrate --run-syncdb

# Создание и заполнение индекса в Elasticsearch
python manage.py search_index --create -f
python manage.py search_index --populate -f

# Запуск Gunicorn
gunicorn doc_service.wsgi --bind=0.0.0.0:8084
