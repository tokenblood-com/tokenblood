# backend for tokenblood project

## Description

## Useful commands

- install dependencies: `poetry install`
- run locally: `poetry run fastapi dev`
- run linters: `make check`
- run tests: `make test`
- build docker image: `cd .. && docker build -t tokenblood-com/backend -f backend/Dockerfile . && cd backend`
- run docker container: `docker run -p 8000:8000 --env-file .env tokenblood-com/backend`



## Debugging

- swagger ui: `http://localhost:8000/docs`
- openapi json: `http://localhost:8000/openapi.json`
- health check: `http://localhost:8000/health`