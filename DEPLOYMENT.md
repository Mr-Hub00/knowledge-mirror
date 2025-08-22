# Django Fly.io Deployment Guide

## 1. Install Fly CLI & Log In

```sh
# Windows (PowerShell)
iwr https://fly.io/install.ps1 -useb | iex

fly auth login
```

---

## 2. Add a Dockerfile

Create a `Dockerfile` in your project root:

```dockerfile
FROM python:3.13-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential libjpeg-dev zlib1g-dev libfreetype6-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/

RUN python manage.py collectstatic --noinput || true

EXPOSE 8000
CMD ["gunicorn", "mrhub.wsgi:application", "--bind", "0.0.0.0:8000"]
```

---

## 3. Update `settings.py` for Fly.io

- Remove any Render-specific hostname code.
- Add this after your ALLOWED_HOSTS/CSRF setup:

```python
FLY_APP_NAME = os.getenv("FLY_APP_NAME")
if FLY_APP_NAME:
    fly_host = f"{FLY_APP_NAME}.fly.dev"
    if fly_host not in ALLOWED_HOSTS:
        ALLOWED_HOSTS.append(fly_host)
    origin = f"https://{fly_host}"
    if origin not in CSRF_TRUSTED_ORIGINS:
        CSRF_TRUSTED_ORIGINS.append(origin)
```

---

## 4. Initialize Fly App

```sh
fly launch --no-deploy
# Choose your app name (e.g., iamhub), region, and keep Dockerfile
```

---

## 5. Edit `fly.toml`

Make sure it looks like this (adjust `app = "iamhub"`):

```toml
app = "iamhub"
primary_region = "iad"

[build]
  dockerfile = "Dockerfile"

[http_service]
  internal_port = 8000
  force_https = true
  auto_stop_machines = "off"
  auto_start_machines = true
  min_machines_running = 1
  processes = ["app"]

  [http_service.concurrency]
    type = "requests"
    hard_limit = 40
    soft_limit = 20

  [[http_service.checks]]
    interval = "10s"
    timeout = "2s"
    grace_period = "20s"
    method = "GET"
    path = "/storacha/health"

[deploy]
  release_command = "python manage.py migrate"
```

---

## 6. (Optional) Add a Database

```sh
fly postgres create --name iamhub-db --regions iad --vm-size shared-cpu-1x --initial-cluster-size 1
fly postgres attach iamhub-db --app iamhub
```

---

## 7. Set Secrets (Environment Variables)

```sh
fly secrets set `
  DJANGO_SECRET_KEY=1wTfL0zNAHmo7wNqHNGn1tt7ZN074vKGxsdVwR8W5rIWCBEjDl `
  DEBUG=False `
  ALLOWED_HOSTS=iamhub.fly.dev,iamhub.net,www.iamhub.net `
  CSRF_TRUSTED_ORIGINS=https://iamhub.fly.dev,https://iamhub.net,https://www.iamhub.net `
  STORACHA_ENABLED=True `
  STORACHA_SPACE_DID=did:key:z6MkkYs8Hoo6cXHbfjH7mQPKzVz7D6hz4nBjCyNRxmCcqsCA
```

---

## 8. Deploy

```sh
fly deploy
```

Check logs:

```sh
fly logs
```

---

## 9. Test

Visit:  
`https://iamhub.fly.dev/storacha/health`  
You should see a JSON response.

---

## 10. Add Custom Domains (when ready)

```sh
fly certificates add iamhub.net
fly certificates add www.iamhub.net
```

Point your DNS as instructed by Fly.io.

---

## 11. Handy Operations

- Scale:
  ```sh
  fly scale count 1
  fly scale memory 256
  ```
- SSH in:
  ```sh
  fly ssh console
  python manage.py createsuperuser
  ```

---

# Django Local Docker Compose Deployment Guide

---

## 1. Prerequisites

- [Docker Desktop](https://www.docker.com/products/docker-desktop/) installed
- (Optional) [Python](https://www.python.org/downloads/) and `pip` for local dev

---

## 2. Project Structure

```
mrhub/
├── core/
├── mrhub/
│   ├── settings.py
│   ├── .env
│   └── ...
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
└── DEPLOYMENT.md
```

---

## 3. Docker Compose Setup

**docker-compose.yml:**
```yaml
services:
  db:
    image: postgres:15
    environment:
      POSTGRES_DB: mrhub
      POSTGRES_USER: mrhub
      POSTGRES_PASSWORD: mrhub
    volumes:
      - pgdata:/var/lib/postgresql/data

  web:
    build: .
    command: gunicorn mrhub.wsgi:application --bind 0.0.0.0:8000 --workers 3
    working_dir: /code
    ports:
      - "8000:8000"
    env_file:
      - ./.env
    volumes:
      - .:/code
    depends_on:
      - db

volumes:
  pgdata:
```

---

## 4. Environment Variables

**.env** (example for local dev):
```
DEBUG=True
DJANGO_SECRET_KEY=dev-only-not-for-prod
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1
CSRF_TRUSTED_ORIGINS=http://localhost:8000,http://127.0.0.1:8000
DATABASE_URL=postgres://mrhub:mrhub@db:5432/mrhub
```

---

## 5. Pin Django Version

In `requirements.txt`:
```
Django==4.2.23
psycopg2-binary
# ...other dependencies...
```

---

## 6. Useful Commands

```powershell
docker compose up --build
docker compose up -d
docker compose logs -f web
docker compose exec web python manage.py migrate
docker compose exec web python manage.py createsuperuser
docker compose exec web python manage.py collectstatic --noinput
docker compose down
```

---

## 7. Favicon (Optional)

- Place `favicon.ico` in `core/static/`
- Add to your base template:
  ```html
  <link rel="icon" href="{% static 'favicon.ico' %}">
  ```
- Collect static files:
  ```powershell
  docker compose exec web python manage.py collectstatic --noinput
  ```

---

## 8. Healthcheck (Optional)

Add to `docker-compose.yml` under `web:`:
```yaml
healthcheck:
  test: ["CMD", "curl", "-fsS", "http://localhost:8000/health/"]
  interval: 30s
  timeout: 5s
  retries: 3
```

---

## 9. Checklist

- [ ] Removed `version:` from compose
- [ ] Django version pinned in `requirements.txt`
- [ ] Gunicorn used for production-ish runs
- [ ] `.env` present and loaded
- [ ] (Optional) favicon added
- [ ] `docker compose up --build` shows no errors

---

**You’re now ready for robust local Docker Compose Django development! 🚀**