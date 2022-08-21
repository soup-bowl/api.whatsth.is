# What's This? API

[![CodeFactor](https://www.codefactor.io/repository/github/soup-bowl/api.whatsth.is/badge)][cf]
[![Gitpod](https://img.shields.io/badge/open%20in-Gitpod-orange?logo=gitpod&logoColor=white)][gp]

**:warning: in active development, thar be dragons!**

Counterpart backend API for the [whatsth.is project][fnt]. It currently has the following functions

* Website technology inspection ([follows this definition file][def]).
* DNS record inspection at a high level.

Want to quickstart? With **Docker/Podman** installed, Run
`docker run -p 43594:43594 ghcr.io/soup-bowl/whatsthis-api:latest` to get going immediately.

To see the endpoints this API supports, visit the `/docs` page ([localhost:43594/docs](http://localhost:43594/docs)).

## Overrides

You can over-ride the default API settings using environmental variables.

Environmental Key      | Default                   | Purpose
-----------------------|---------------------------|--------
`REDIS_URL`            | *None (required)*         | Caching & storage agent. 
`WTAPI_DEFINITION_URL` | [Latest definitions][def] | Can provide a different YAML or JSON source for the detection definitions.
`WTAPI_CORS_POLICY`    | `*`                       | Define a forced origin. Only supports **1 origin** at the moment.

## Starting up

Use **Uvicorn** to run the server asynchronously. This is achieved by running the following (post depedency installation
- see below):

```bash
uvicorn api.main:app --reload
```

By default, the server will be available at http://localhost:8000 and auto API docs on http://localhost:8000/docs. Stack
is built to expect port 43594, so you would benefit from adding `--port 43594` to your Uvicorn run statement.

### Docker

Run `docker-compose up --build` to start the server locally (runs on port 43594).

### Native

This project uses [Poetry](https://python-poetry.org/) to manage dependencies.

```bash
poetry install
poetry run uvicorn api.main:app --reload --port 43594
```

To run the unit tests, run `poetry run pytest`, and to lint the codebase, run `pylint` by executing
`poetry run pylint --recursive=y api`.

[cf]:  https://www.codefactor.io/repository/github/soup-bowl/api.whatsth.is
[gp]:  https://gitpod.io/#https://github.com/soup-bowl/whatsth.is
[fnt]: https://github.com/soup-bowl/whatsth.is
[def]: https://gist.github.com/soup-bowl/ca302eb775278a581cd4e7e2ea4122a1#file-definitions-yml
