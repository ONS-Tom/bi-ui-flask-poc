# bi-ui-flask-poc

[![phase](https://img.shields.io/badge/phase-BETA-orange.svg)](https://img.shields.io/badge/phase-BETA-orange.svg) [![license](https://img.shields.io/github/license/mashape/apistatus.svg)](./LICENSE)

A proof of concept of the Business Index User Interface using Flask.

Previous repository: https://github.com/ONSdigital/bi-ui

### Table of Contents
**[1. Environment Setup](#environment-setup)**<br>
**[2. Running Instructions](#running-instructions)**<br>
**[3. Testing](#testing)**<br>
**[4. Dependencies](#dependencies)**<br>
**[5. Troubleshooting](#troubleshooting)**<br>
**[6. Contributing](#contributing)**<br>
**[7. License](#license)**<br>

## Environment Setup

Firstly, install Python 3:

```shell
brew install python
```

Create a virtual environment (from inside the cloned repository):

```shell
python3 -m venv venv
```

## Running Instructions

Activate the virtual environment:

```shell
source venv/bin/activate
```

Install dependencies from the `requirements.txt` file:

```shell
pip install -r requirements.txt
```

Run the server in development mode, with hot-reloading:

```shell
FLASK_APP=run.py FLASK_DEBUG=1 ENVIRONMENT=DEV python3 -m flask run
```

The user interface can be accessed on http://localhost:5000.

## Testing

## Dependencies

* [flask-login](http://flask-login.readthedocs.io/en/latest/)
* [flask-session](http://flask-session.readthedocs.io/en/latest/)
* [flask-restful](http://flask-restful.readthedocs.io/en/latest/)

## Troubleshooting

If your updates to static files aren't registering, reset the cache (shift + press refresh in Chrome).

## Contributing

See [CONTRIBUTING](./CONTRIBUTING.md) for details.

## License

Copyright ©‎ 2018, Office for National Statistics (https://www.ons.gov.uk)

Released under MIT license, see [LICENSE](./LICENSE) for details.