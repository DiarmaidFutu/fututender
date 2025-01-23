# FutuTender

An application to view EU tenders that are of interest to Futurice sales

## Docker

starting up:

```
docker compose up --build
```

tearing down:
```
docker compose down -v
```

## Adding migrations: 

```
docker compose exec web alembic revision --autogenerate -m "message goes here"
```
