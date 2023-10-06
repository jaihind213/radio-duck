# Radio-Duck
A duckDb server, you can talk to.

![Project Image](radioduck.png)

## Project Objectives

- Talk to duckDb over transport protocols like Http.
- Provide an alternative to embedding duckDb
- Make DuckDb highly available for apps like Business intelligence dashboards
- Ability to query data while data is being loaded.

## Use cases

- Act as database server for Business intelligence dashboards like (metabase/superset) without embedding duckDb

## Features

### Run sql on Duckdb over http

#### Run sql
You can send a sql via http post request. refer to docs @ http://localhost:8000/docs

#### Transaction support
It's possible but in a limited fashion (i.e. in a single http post request)
Ideally radio-duck sql run_sql endpoint should not be used for writes. 
We plan to have another endpoint for loading data.
```bash
#example:
curl -X 'POST' \
  'http://localhost:8000/v1/sql/' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "sql": "BEGIN; select * from pond; COMMIT;"
}'
```

### Load data from cloud blob storage like s3/azure 
[todo]

### Consume data from streams like kafka 
[todo]

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

- todo: handle large datasets / compress results say json-smile?
- todo: limit number of conns to duckdb ?
- todo: add python styling enforcer to project
- todo: return query_id ,useful for debugging.
- todo: handle transactions over http ? i.e. multiple http requests.