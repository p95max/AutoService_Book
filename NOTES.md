docker compose exec web python manage.py makemigrations service_book
docker compose exec web python manage.py migrate --noinput
docker compose exec web python manage.py showmigrations

docker compose exec web python manage.py loaddata service_book/fixtures/brands.json


docker compose build --no-cache 
docker compose up -d --force-recreate 
docker compose logs -f

