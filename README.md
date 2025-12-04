🚗 AutoService Book

**AutoService Book** is your reliable assistant for tracking and managing your car’s service history.
This web application, built as a portfolio project, showcases skills in Django development, database management,
and creating user-friendly interfaces.

## About

AutoService Book is designed for car owners who want to:
- Keep detailed records of all maintenance and repair work.
- Store information about oil changes, inspections, repairs, and fuel expenses.
- View complete service and expense history in one convenient place.
- Stay on top of upcoming services and monitor costs.

With a clean and intuitive interface, you can easily:
- Add and edit service records.
- Manage fuel expenses and track consumption.
- Record purchased and installed car parts.
- View service history for each vehicle.
- Analyze average fuel consumption and remaining fuel.
- Manage multiple cars from a personal dashboard.
- Export data to CSV tables.

AutoService Book brings organization, transparency, and ease to your car ownership experience.

## Deployment & Architecture

- **Dockerized:** The entire project is containerized with Docker for easy deployment and reproducibility.
- **Nginx:** Nginx is used as a reverse proxy for serving static files and handling client requests efficiently.
- **PostgreSQL:** The production database runs as a managed cloud instance, separate from the application container.

This setup reflects a real-world production architecture and demonstrates skills in modern backend deployment.

## Features

- 🛠️ **Track Service History and Car Parts**: Add, edit, and delete service and part records.
- 🚗 **Manage Vehicles**: Keep track of multiple cars with details (brand, model, year, mileage, VIN).
- 🔋 **Monitor Fuel Expenses**: Record fuel purchases, calculate distances, and track costs.
- ⛽ **Check Fuel Levels and Consumption**: Automatically calculate remaining fuel and average consumption.
- 📊 **Analyze Expenses**: View all expenses and service history in one place.
- 📥 **CSV Export**: Download service, fuel, part, and other expense data as CSV files.
- 🌗 **Dark/Light Theme Switcher**: Toggle between light and dark themes for a comfortable experience.
- 🔐 **Authorisation** by Google available

## Tech Stack

- **Backend:** Django 5.2, Python 3.14
- **Frontend:** Bootstrap 5 (via `crispy-bootstrap5`), HTML, CSS, JavaScript
- **Database:** PostgreSQL 16 (managed cloud instance)
- **Authentication:** `django-allauth` for email-based login
- **Caching:** Django Cache Framework for optimized queries
- **Additional:** Django signals for automatic mileage and fuel updates, CSV export functionality
- **Production:** Docker, Nginx, Render.com

## Usage

1. **Sign Up/Login:** Register or log in via email using `django-allauth`.
2. **Add Vehicles:** Go to the "Autos" section to add cars (brand, model, year, mileage, VIN).
3. **Manage Records:**
   - Add service records, fuel expenses, car parts, or other expenses.
   - View detailed history and analytics for each car.
   - Export data to CSV for offline use.
4. **Monitor Fuel:** Check remaining fuel and average consumption on the dashboard.
5. **Toggle Themes:** Switch between dark and light themes for a better experience.


## Startup & Entry Script (Docker)

This project uses an entry script (`entrypoint.sh`) to bootstrap the app in containers. It’s **idempotent**
and safe to run on every container start.

### What the script does
1. **Waits for the database** using the `DATABASE_URL` (TCP check with timeout/retries).
2. **(Dev only) Auto generate migrations** if `AUTO_MAKEMIGRATIONS=1`.
3. **Apply migrations**: `python manage.py migrate --noinput`.
4. **Load fixtures (brands)** only if the table is empty (or forcibly, if requested).
5. **Optional table sanity check** via `CHECK_TABLE` env.
6. **Collect static files**: `python manage.py collectstatic --noinput`.
7. **Ensure superuser** with `manage.py createsuperuser --noinput` (idempotent).

### Environment variables
- `DATABASE_URL`: PostgreSQL DSN, e.g. `postgres://app:pass@db:5432/app`.
- `AUTO_MAKEMIGRATIONS` (dev): set to `1` to run `makemigrations` on start.
- `FIXTURE_BRANDS`: path to the brands fixture **inside** the container. Default:
  ```
  /app/service_book/fixtures/brands.json
  ```
- `LOG_FIXTURES`: set to `1` to log fixture operations verbosely.
- `FORCE_BRANDS_LOAD`: set to `1` to truncate and reload brands from fixture.
- `CHECK_TABLE`: optional table name to assert existence, e.g. `public.service_book_brand`.
- `DJANGO_SUPERUSER_USERNAME`, `DJANGO_SUPERUSER_EMAIL`, `DJANGO_SUPERUSER_PASSWORD`: superuser bootstrap credentials.
- `DJANGO_SETTINGS_MODULE`, `DJANGO_WSGI_MODULE`: Django settings and WSGI module (e.g., `autoservice_book.settings`, `autoservice_book.wsgi`).

### Snippet (core logic)
```sh
# Wait DB (via DATABASE_URL), then:
[ "${AUTO_MAKEMIGRATIONS:-0}" = "1" ] && python manage.py makemigrations || true
python manage.py migrate --noinput

# Load brands fixture (idempotent; can be forced)
: "${FIXTURE_BRANDS:=/app/service_book/fixtures/brands.json}"
# Python block checks table existence and loads with loaddata only when needed.

# Optional table check (prints regclass)
# CHECK_TABLE=public.service_book_brand

python manage.py collectstatic --noinput

# Ensure superuser
if [ -n "$DJANGO_SUPERUSER_USERNAME" ] && [ -n "$DJANGO_SUPERUSER_EMAIL" ] && [ -n "$DJANGO_SUPERUSER_PASSWORD" ]; then
  python manage.py createsuperuser --noinput || true
fi
```

### Google OAuth (allauth) quick note
Create an **OAuth client (Web)** in Google Cloud and set:
- Redirect URI (dev): `http://localhost:8000/accounts/google/login/callback/`
- Redirect URI (prod): `https://<your-domain>/accounts/google/login/callback/`

Then export:
```
GOOGLE_CLIENT_ID=xxxx.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=yyyy
```
You can alternatively configure a **SocialApp (Google)** in Django Admin and bind it to your Site.

## Portfolio Notes

This project was built to demonstrate:
- Proficiency in Django, including models, views, forms, and signals.
- Database design and management with PostgreSQL.
- User authentication and security with `django-allauth`.
- Responsive UI with Bootstrap 5 and `crispy-forms`.
- Performance optimization using caching.
- Data export functionality with CSV.
- Modern deployment with Docker, Nginx, and cloud database.

Feel free to explore the code, test the app, or provide feedback!

## Contributing

This is a portfolio project, but suggestions or feedback are welcome! Feel free to open an issue or submit a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.