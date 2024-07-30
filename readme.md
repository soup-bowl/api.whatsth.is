# What's This? API

[![CodeFactor](https://www.codefactor.io/repository/github/soup-bowl/api.whatsth.is/badge)][cf]
[![Gitpod](https://img.shields.io/badge/open%20in-Gitpod-orange?logo=gitpod&logoColor=white)][gp]

**:warning: in active development, thar be dragons!**

Counterpart backend API for the [whatsth.is project][fnt]. It currently has the following functions

* Website technology inspection ([follows this definition file][def]).
* DNS record inspection at a high level.

Want to quickstart? With **Docker/Podman** installed, Run:

```docker run -p 80:80 ghcr.io/soup-bowl/api:latest```

This API has Swagger documentation on the homepage.

## Overrides

You can over-ride the default API settings using environmental variables.

Environmental Key      | Default                   | Purpose
-----------------------|---------------------------|--------
`REDIS_URL`            | *None*                    | Caching & storage agent. 
`WTAPI_DEFINITION_URL` | [Latest definitions][def] | Can provide a different YAML or JSON source for the detection definitions.

## Starting up

Use **Kestrel** to run the server. This is achieved by running the following (post depedency installation - see below):

```bash
dotnet run --project Whatsthis.API
```

By default, the server will be available at http://localhost:43594.

### Docker

Run `docker-compose up --build` to start the server locally (runs on port 43594).

### Native

This project uses NuGet to manage dependencies.

```bash
dotnet dev-certs https 
dotnet restore
dotnet build
dotnet run --project Whatsthis.API
```

This project uses **xUnit** for tests, and can be run by executing:

```bash
dotnet test
```

[cf]:  https://www.codefactor.io/repository/github/soup-bowl/api.whatsth.is
[gp]:  https://gitpod.io/#https://github.com/soup-bowl/whatsth.is
[fnt]: https://github.com/soup-bowl/whatsth.is
[def]: https://gist.github.com/soup-bowl/ca302eb775278a581cd4e7e2ea4122a1
