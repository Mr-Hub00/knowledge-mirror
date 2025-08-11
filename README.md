# IAMHUB Cosmic Hub

A Django-powered cosmic/starfield themed portal.

## Quick Start

1. **Clone & Install**
   ```bash
   git clone https://github.com/yourusername/iamhub.git
   cd iamhub
   python -m venv venv
   venv\Scripts\activate  # Windows
   pip install -r requirements.txt
   ```

2. **Environment Setup**
   - Copy `.env.sample` to `.env` and fill in secrets:
     ```
     DJANGO_SECRET_KEY=your-secret-key
     DJANGO_DEBUG=True
     DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1
     ```

3. **Database & Static Files**
   ```bash
   python manage.py migrate
   python manage.py collectstatic --noinput
   ```

4. **Run Dev Server**
   ```bash
   python manage.py runserver
   ```

5. **Admin**
   ```bash
   python manage.py createsuperuser
   # Visit /admin/ to add projects
   ```

## Production

- Set `DJANGO_DEBUG=False` and update `DJANGO_ALLOWED_HOSTS`.
- Run `python manage.py check --deploy`.
- Use WhiteNoise for static files (already configured).
- Logs are in `/logs/django.log`.

## Features

- Cosmic starfield theme (CSS parallax, glow, day/night toggle)
- Projects list/detail (admin managed)
- Contact form (DB stored)
- Auth: login, signup, protected dashboard
- Accessible, SEO-friendly, responsive

## Formatting

- CSS/HTML: Prettier or EditorConfig recommended.

## Useful Django & Refresh Commands

### Run the development server
```bash
python manage.py runserver
```

### Apply migrations
```bash
python manage.py migrate
```

### Make migrations for an app
```bash
python manage.py makemigrations indexapp
```

### Collect static files (for WhiteNoise or production)
```bash
python manage.py collectstatic --noinput
```

### Create a superuser for admin
```bash
python manage.py createsuperuser
```

### Hard refresh your browser
- Windows: `Ctrl + Shift + R` or `Ctrl + F5`
- Mac: `Cmd + Shift + R`

python manage.py collectstatic --noinput
python manage.py runserver

## License
