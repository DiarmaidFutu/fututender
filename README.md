# FutuTender

An application to view EU tenders that are of interest to Futurice sales

## starting docker

```
docker compose up --build
```

## Adding migrations: 

```
docker compose exec web alembic revision --autogenerate -m "message goes here"
```
