# What's This? API

Counterpart backend API for the [whatsth.is project](https://github.com/soup-bowl/whatsth.is). Feed it a URL, and it returns a bunch of details about the requested site.

## Starting up

By default, the server will be available at http://localhost:43594.

### Docker

Run `docker-compose up --build` to start the server locally.

### Native

This uses virtual ENV to help keep dependencies away from the system.

```bash
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt
```

Now the server can begin (when in the virtual env) by running `python -m api`.
