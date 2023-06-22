## Admin Panel
http://work-hours.localhost

Login and Password - admin@admin.com admin

## Dowloand Docker Debian

https://docs.docker.com/engine/install/debian/

## Start Projects localhost

```
docker compose up
```

http://work-hours.localhost

## Prod Projects domain

!!!Link domain to vds!!!

Change in docker compose and settings domain work-hours.localhost to domain.ru

docker-compose.yml

```
  backend:
      build:
        dockerfile: src/backend/Dockerfile
        context: .
      command: >
        sh -c "python manage.py migrate && python manage.py collectstatic --noinput && gunicorn settings.wsgi:application --bind 0.0.0.0:8776"
      labels:
        - "traefik.enable=true"
        - "traefik.docker.network=web"
        - "traefik.http.routers.backend.rule=Host(`work-hours.localhost`)" ### replace -> - "traefik.http.routers.backend.rule=Host(`domain.ru`)"
        - "traefik.http.services.backend.loadbalancer.server.port=8776"
      networks:
        - web
```

src/backend/settings/settings.py

```
CSRF_TRUSTED_ORIGINS = [
    'http://127.0.0.1:8776',
    'https://work-hours.localhost'  ### replace -> 'https://domain.ru'
]

CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOWED_ORIGINS = [
    'http://127.0.0.1:8776',
    'https://work-hours.localhost' ### replace -> 'https://domain.ru'
]

```

### Prod

```
docker compose up
```