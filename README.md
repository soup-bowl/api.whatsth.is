# What's This? API

[![CodeFactor](https://www.codefactor.io/repository/github/soup-bowl/api.whatsth.is/badge)](https://www.codefactor.io/repository/github/soup-bowl/api.whatsth.is)

Counterpart backend API for the [whatsth.is project](https://github.com/soup-bowl/whatsth.is). Feed it a URL, and it returns a bunch of details about the requested site.

The API operates on a detection configuration file.

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

To run the unit tests, install `pytest` (`pip install pytest`) and run `pytest`.
