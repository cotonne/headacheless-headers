# Unsecure Server

The aim of this application is to teach why and how configure important HTTP headers related to security.

# Development

## Installation

```bash
$ python3 -m venv venv
$ source venv/bin/activate
$ pip install -r requirements.txt
$ python create_cert.py
```

## Run

```bash
$ . venv/bin/activate
$ export FLASK_APP=unsecure
$ export FLASK_ENV=development
$ flask run
 * Running on http://127.0.0.1:5000/
$ firefox http://127.0.0.1:5000/
```

## Run with SSL

```
$ flask run --cert=selfsigned.crt --key=private.key
```

 - [Evercookies & Cookies Zombies](https://developer.mozilla.org/fr/docs/Web/HTTP/Cookies#cookies_zombie_et_evercookies)
