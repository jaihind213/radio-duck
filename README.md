# Radio-Duck
Connect to a Duckdb server over Http.

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
#pull from docker hub
docker pull jaihind213/radio-duck:latest
# or build
sh buildDocker.sh
docker run -p 8000:8000 -t jaihind213/radio-duck:latest
#or
docker run -p 8000:8000 -v <path_to_data_dir>:/radio-duck/pond -t jaihind213/radio-duck:latest
#or
docker run -p 8000:8000 -v <path_to_data_dir>:/radio-duck/pond -v <path_to_my_config.ini>:/radio-duck/pond/my_config.ini -t jaihind213/radio-duck:latest python /radio-duck/server.py /radio-duck/pond/my_config.ini

#are u on mac m1, change buildDocker.sh a bit. uncomment & comment a build-line in it.
```
Then access http://localhost:8000/docs and play with the api.

## Try me with Apache Superset
```
#run radio-duck
docker run -p 8000:8000 -t jaihind213/radio-duck:latest
#run superset
docker pull jaihind213/superset-radioduck:latest
docker run -e TALISMAN_ENABLED="False" -e ADMIN_USERNAME=admin -e ADMIN_PASSWORD=admin -e SUPERSET_SECRET_KEY=<some_good_key> -p 8088:8088 jaihind213/superset-radioduck:latest
```
Then access http://localhost:8088/

Then configure database with alchemy URI 'radio_duck+district5://user:pass@<HOST_IP>:8000/?api=/v1/sql/&scheme=http'

<span style="color:red;">Video of Demo</span>.

[![Demo](demo_thumbnail.png)](https://youtu.be/GUBj2uzly94?si=2QZm4WWnARM1kwgv "Demo video")

## Try me with Python code via District5 library

https://github.com/jaihind213/district5
```
#python 3.9^
pip install district5
#start the duckdb server i.e. radio-duck
docker run -p 8000:8000 -t jaihind213/radio-duck:latest
#the duckdb starts up with a sample table whose ddl is: 
#'create table pond(duck_type string, total int)'
echo "we will try to query that"
```

```

from sqlalchemy import create_engine, text
from sqlalchemy.dialects import registry

registry.register(
    "radio_duck.district5", "radio_duck.sqlalchemy", "RadioDuckDialect"
)


#run docker instance of radio-duck
#docker run -p 8000:8000 -t jaihind213/radio-duck:latest
engine = create_engine(
    "radio_duck+district5://user:pass@localhost:8000/?api=/v1/sql/&scheme=http"
)
# Establish a database connection
conn = engine.connect()

# Define a SQL query using qmark style or positional style
try:
    query_1 = text("""SELECT duck_type, total FROM pond where total > :total""")
    params = {"total": 0}
    result = conn.execute(query_1, params)
    # Fetch and print the results
    for row in result:
        print(row)

    print("--------------")
    query_2 = "SELECT duck_type, total FROM pond where total > ?"
    result = conn.execute(query_2, (0,))

    for row in result:
        print(row)

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    # Close the database connection
    conn.close()
    engine.dispose()

```

### Check for Docker image Vulnerabilities
```
sh buildDocker.sh <version>
sh docker_sec_check.sh
# github actions is scanning for Vulnerabilities
```

## Notes:

- todo: stream large datasets / compress results say json-smile?
- todo: limit number of conns to duckdb ?
- todo: return query_id ,useful for debugging.
- todo: handle transactions over http ? i.e. multiple http requests.
- todo: load data api from s3/azure blob storage
