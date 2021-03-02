# Backend

---

## Iniciar los contenedores
```console
$ docker-compose build

$ docker-compose up -d
```
## Pruebas 
```console
$ docker-compose exec api pytest --disable-warnings --cov=app --cov-report=html
```

## Puertos y URLS
- __API__: `8080`
    - SwaggerUI docs: http://localhost:8080/docs
    - ReDoc: http://localhost:8080/redoc