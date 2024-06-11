
## Development

- Install from source code

Before you can use `apsbot`, you need to install it. Clone the repository and install it using pip:

```bash
pip install git+https://github.com/chuongmep/aps-bot.git --upgrade
```
or clone the repository and install it using pip:

```bash
pip install . --upgrade
```

## Requirements 

Setup environment variables

```bash
APS_CLIENT_ID = "your_client_id"
APS_CLIENT_SECRET = "your_client_secret"
OPENAI_API_KEY = "your_openai_api_key"
```

## Build Local Package


Build package with setuptools
```bash
python setup.py sdist bdist_wheel
```

Update new version package 

```bash
python setup.py sdist bdist_wheel
python -m twine check dist/*
python -m twine upload dist/*
```

## Quick Testing 

```bash
pip install --editable . --user
```