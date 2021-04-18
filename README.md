# Backend

[![CodeBuild](https://codebuild.us-east-1.amazonaws.com/badges?uuid=eyJlbmNyeXB0ZWREYXRhIjoiVzNCUDVBdU9WdDQxWkw1bFBXY1EvWFpqbVVlc3FtTm1YMXI2Rm82MUs0eTBzcm5DVGtuTy9xaEM2bnRldHhUVml4Rm5QKzVLY2FnWVk1Q2FRb3lyQmVjPSIsIml2UGFyYW1ldGVyU3BlYyI6IkU4amtDZ0pieEs2ZWpvSkkiLCJtYXRlcmlhbFNldFNlcmlhbCI6MX0%3D&branch=main)]()
[![Black Formatting](https://github.com/Tall-Programacion-FIME/backend/actions/workflows/main.yml/badge.svg)](https://github.com/Tall-Programacion-FIME/backend/actions/workflows/main.yml)

## Iniciar los contenedores
```console
$ docker-compose build

$ docker-compose up -d
```
## Pruebas 
```console
$ docker-compose exec api pytest --cov=app --cov-report=html
```

## Puertos y URLS
- __API__: `8080`
    - SwaggerUI docs: http://localhost:8080/docs
    - ReDoc: http://localhost:8080/redoc
