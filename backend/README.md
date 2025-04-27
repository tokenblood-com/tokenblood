# backend for tokenblood project

## Description

## Useful commands

- install dependencies: `poetry install`
- run locally: `poetry run fastapi dev`
- run linters: `make check`
- build docker image: `docker build -t tokenblood-backend .`
- run docker container: `docker run -d -p 8000:8000 --name tokenblood-backend tokenblood-backend`



## Debugging

- swagger ui: `http://localhost:8000/docs`
- openapi json: `http://localhost:8000/openapi.json`
- health check: `http://localhost:8000/health`