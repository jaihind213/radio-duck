# Radio-Duck
A duckDb server, you can talk to.

![Project Image](radioduck.png)

## Project Objectives

- Talk to duckDb over transport protocols like Http.
- Provide an alternative to embedding duckDb
- Make DuckDb highly available for apps like Business intelligence dashboards
- Ability to query data while data is being loaded.
``
## Use cases

- Act as database server for Business intelligence dashboards like (metabase/superset) without embedding duckDb

## Features

- Run sql on Duckdb over http [wip]
- Load data from cloud blob storage like s3/azure [todo]
- Consume data from streams like kafka [todo]

## Requirements

- install mamba https://mamba.readthedocs.io/en/latest/
- install docker

```
cd PROJECT_DIR
mamba create -n radio-duck python=3.10
mamba activate radio-duck
mamba install poetry
poetry install
```

## Run Tests
```
pytest
```

## Try me with Docker
```
sh buildDocker.sh
docker run -p 8000:8000 -t jaihind213/radio-duck:latest
#or
docker run -p 8000:8000 -v <path_to_data_dir>:/radio-duck/pond -t jaihind213/radio-duck:latest
#or
docker run -p 8000:8000 -v <path_to_data_dir>:/radio-duck/pond -v <path_to_my_config.ini>:/radio-duck/pond/my_config.ini -t jaihind213/radio-duck:latest python /radio-duck/server.py /radio-duck/pond/my_config.ini

#are u on mac m1, change buildDocker.sh a bit. uncomment & comment a build-line in it.
```
Then access http://localhost:8000/docs

### Check for Docker image Vulnerabilities
```
sh buildDocker.sh
sh docker_sec_check.sh
#feel free to fail build if u find some vulnerabilities! 
```

## Notes:

- <todo> handle large datasets / compress results say json-smile?
- <todo> limit number of conns to duckdb ?