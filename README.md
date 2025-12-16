🚗 AutoService Book

AutoService Book is `a Django web application` designed to manage car service records, fuel logs, parts, and related expenses.
Built as a portfolio project, it highlights hands-on experience with Django (forms, models, auth, i18n), database design, data validation, pagination, and a maintainable, user-oriented interface.

---

## Features

- 🛠️ **Track Service History and Car Parts**: Add, edit, and delete service and part records.
- 🚗 **Manage Vehicles**: Keep track of multiple cars with details (brand, model, year, mileage, VIN).
- 🔋 **Monitor Fuel Expenses**: Record fuel purchases, calculate distances, and track costs.
- ⛽ **Check Fuel Levels and Consumption**: Automatically calculate remaining fuel and average consumption.
- 📊 **Analyze Expenses**: View all expenses and service history in one place.
- 📥 **CSV Export**: Download service, fuel, part, and other expense data as CSV files.
- 🌗 **Dark/Light Theme Switcher**: Toggle between light and dark themes for a comfortable experience.
- 🔐 **Authorisation** by Google available
- 🌍 **Localization by i18n**: full German🇩🇪 UI translation added (🇬🇧 as default) with a convenient language switcher

---

## Tech Stack

- **Backend:** Django 5.2, Python 3.14
- **Frontend:** Bootstrap 5 (via `crispy-bootstrap5`), HTML, CSS, JavaScript
- **Database:** PostgreSQL 16 (managed cloud instance)
- **Authentication:** `django-allauth` for email-based login
- **Caching:** Django Cache Framework for optimized queries
- **Additional:** Django signals for automatic mileage and fuel updates, CSV export functionality
- **Production:** Docker
- **Localization** i18n

---

## Usage

1. **Sign Up/Login:** Register or log in via email using `django-allauth`.
2. **Add Vehicles:** Go to the "Autos" section to add cars (brand, model, year, mileage, VIN).
3. **Manage Records:**
   - Add service records, fuel expenses, car parts, or other expenses.
   - View detailed history and analytics for each car.
   - Export data to CSV for offline use.
4. **Monitor Fuel:** Check remaining fuel and average consumption on the dashboard.
5. **Toggle Themes:** Switch between dark and light themes for a better experience.

---

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

---

## Environment (.env)

Copy `.env.example` to `.env` and adjust values.

Docker Compose will pick it up if you add `env_file: .env` (or map specific `environment:` keys).

**Key variables in `.env.example`:**
- `ALLOWED_HOSTS`
- `DJANGO_SUPERUSER_USERNAME`
- `DJANGO_SUPERUSER_EMAIL`
- `DJANGO_SUPERUSER_PASSWORD`
- `GOOGLE_CLIENT_ID`
- `GOOGLE_CLIENT_SECRET`

```yaml
services:
  web:
    env_file: .env
    # or supply a subset explicitly:
    # environment:
    #   DATABASE_URL: ${DATABASE_URL}
    #   DJANGO_SETTINGS_MODULE: ${DJANGO_SETTINGS_MODULE}
```

---

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

---

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

---

### Localization (EN / DE)

The application ships with full German localization 🇩🇪 while English remains the default language 🇬🇧.
- All UI texts are translated via Django i18n (.po/.mo)
- Language switcher is available in the navigation bar
- User language preference is stored in session
- Seamless switching without page reload issues

#### Quick dev guide

Make sure the following `settings` are enabled:
```
USE_I18N = True
USE_L10N = True

LANGUAGES = [
    ("en", "English"),
    ("de", "Deutsch"),
]

LOCALE_PATHS = [BASE_DIR / "locale"]
```

1. To update translations:
```bash
python manage.py makemessages -l de
```
2. Edit `locale/de/LC_MESSAGES/django.po`
3. To compile(save) translations:
```bash
django-admin compilemessages
```
4. (Optional) Recreate docker container
```bash
docker compose down -v
docker compose up --build
```

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## Roadmap / TODO
- [x] One-command service startup via Docker Compose (`docker compose up --build`)
- [x] Comprehensive container init script (`entrypoint.sh`)
- [x] Fixture set for fast, end-to-end service testing (`fixtures/`)
- [x] Hide the admin URL in urls via .env
- [x] Auth via Google (OAuth2)
- [ ] Grafana + Prometheus + Alertmanager integration
- [ ] Auth protected with CAPTCHA (django-turnstile)
- [ ] CI for tests/linters (flake8)

- [ ] Snowfall visual effect for the UI (with switcher)

- Test coverage of the service

---

**Author:** Maksym Petrykin  
Email: [m.petrykin@gmx.de](mailto:m.petrykin@gmx.de)  
Telegram: [@max_p95](https://t.me/max_p95)
