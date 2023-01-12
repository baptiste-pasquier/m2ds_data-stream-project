# m2ds_data_stream_project

[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://baptiste-pasquier-m2ds-data-stream-project.streamlit.app/)
[![Build & Test](https://github.com/baptiste-pasquier/m2ds_data-stream-project/actions/workflows/main.yml/badge.svg)](https://github.com/baptiste-pasquier/m2ds_data-stream-project/actions/workflows/main.yml)
[![codecov](https://codecov.io/github/baptiste-pasquier/m2ds_data-stream-project/branch/main/graph/badge.svg)](https://codecov.io/gh/baptiste-pasquier/m2ds_data-stream-project)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

## Prerequities

- Sign-up for a Twitter developer account on this [link](https://developer.twitter.com/en/apply-for-access)
- Create a Bearer Token ([documentation](https://developer.twitter.com/en/docs/authentication/oauth-2-0/bearer-tokens))
- Fill in the field `BEARER_TOKEN` in the `secret_config.yml` file
- Create a Reddit developed application on this [link](https://www.reddit.com/prefs/apps/) ([documentation](https://praw.readthedocs.io/en/stable/getting_started/authentication.html#password-flow))
- Fill in the fields `CLIENT_ID`, `SECRET_TOKEN`, `USERNAME` and `PASSWORD` in the `secret_config.yml` file
- Install and run Kafka ([documentation](https://kafka.apache.org/quickstart))
- Create a MongoDB database in the [cloud](https://www.mongodb.com/cloud/atlas/register) (free) or install the server ([documentation](https://www.mongodb.com/docs/manual/installation/))
- Fill in the fields `CONNECTION_STRING` in the `secret_config.yml` file

## Installation

1. Clone the repository
```bash
git clone https://github.com/baptiste-pasquier/m2ds_data-stream-project
```

2. Install the project
- With `poetry` ([installation](https://python-poetry.org/docs/#installation)) :
```bash
poetry install
```
- With `pip` :
```bash
pip install -e .
```

3. Install pre-commit
```bash
pre-commit install
```

## Usage

> **Warning**
> Each script must be run in a separate console

1. Twitter streaming:
```bash
python scripts/ingest_tweets.py
```

2. Reddit streaming:
```bash
python scripts/ingest_reddit.py
```

3. Data preprocessing:
```bash
python scripts/tsf_data.py
```

4. Data clustering:
```bash
python scripts/cluster_data.py
```

5. Data storage on MongoDB:
```bash
python scripts/store_data.py
```

Run 1 + 2 + 3 + 4 + 5 in parallel:
```bash
python scripts/run_all.py
```

Real-time visualization:
```bash
streamlit run streamlit_app.py
```
