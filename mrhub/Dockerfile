ARG PYTHON_VERSION=3.13-slim

FROM python:${PYTHON_VERSION}

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN mkdir -p /code

WORKDIR /code

COPY requirements.txt /tmp/requirements.txt
RUN set -ex && \
    pip install --upgrade pip && \
    pip install -r /tmp/requirements.txt && \
    rm -rf /root/.cache/
COPY . /code

RUN python manage.py collectstatic --noinput

RUN apt-get update && apt-get install -y ca-certificates

EXPOSE 8000

CMD ["bash", "-lc", "gunicorn mrhub.wsgi:application --bind 0.0.0.0:$PORT"]
