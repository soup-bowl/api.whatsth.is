# What's This? API

[![CodeFactor](https://www.codefactor.io/repository/github/soup-bowl/api.whatsth.is/badge)](https://www.codefactor.io/repository/github/soup-bowl/api.whatsth.is)

**:warning: in active development, do not expect stability!**

Counterpart backend API for the [whatsth.is project](https://github.com/soup-bowl/whatsth.is). Feed it a URL, and it returns a bunch of details about the requested site. Upon execution, the [latest definitions file is downloaded](https://gist.github.com/soup-bowl/ca302eb775278a581cd4e7e2ea4122a1) from GitHub.

Want to quickstart? With **Docker/Podman** installed, Run `docker run -p 43594:43594 ghcr.io/soup-bowl/whatsthis-api:latest` to get going immediately.

Example: `http://localhost:8000/https://wordpress.org` should reply with something like:

```json
{
  "success": true,
  "message": {
    "technology": "WordPress",
    "matched_on": [
      "/html/head/link[@href='//s.w.org']"
    ]
  },
  "url": "https://wordpress.org"
}
```

## Starting up

Use **Uvicorn** to run the server asynchronously. This is achieved by running the following (post depedency installation - see below):

```bash
uvicorn api.main:app --reload
```

By default, the server will be available at http://localhost:8000 and auto API docs on http://localhost:8000/docs.

### Docker

Run `docker-compose up --build` to start the server locally.

### Native

This uses virtual ENV to help keep dependencies away from the system.

```bash
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt
```

Now the server can begin (when in the virtual env) by running `uvicorn api.main:app --reload`.

To run the unit tests, install `pytest` (`pip install pytest`) and run `pytest`.
