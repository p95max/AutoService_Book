docker compose exec web python manage.py makemigrations service_book
docker compose exec web python manage.py migrate --noinput
docker compose exec web python manage.py showmigrations

docker compose exec web python manage.py loaddata service_book/fixtures/brands.json


docker compose up --build --no-cache 
docker compose up -d --force-recreate 
docker compose logs -f

python manage.py makemessages -l de
docker compose exec web python manage.py makemessages -l de

python manage.py compilemessages
docker compose exec web python manage.py compilemessages
