import configparser
import logging
import os

app_config = configparser.SafeConfigParser()


def setup_app_config(default_ini):
    with open(default_ini) as cf:
        app_config.read_file(cf)


def get_config():
    return app_config


# https://spacelift.io/blog/docker-secrets
def configure_sekrets(connection):
    """
    sekret aka secret :)
    :return: None
    """
    sekret_file = get_config().get(
        "duck", "sekret_file", fallback="/run/secrets/duck_sekrets"
    )

    if os.path.isfile(sekret_file):
        # if file not there error todo
        logging.info("configuring secrets")
        with open(sekret_file, "r") as file:
            for line in file:
                if not line.lstrip().startswith("#"):
                    k, v = line.strip().split("=", 1)
                    # duckdb specific
                    # accesskeys/ secretkeys must have prefix duck_
                    if k.startswith("duck_"):
                        parameter = k[len("duck_") :]  # noqa: E203
                        query = "set global {}='{}';".format(parameter, v)
                        connection.execute(query)
                    else:
                        os.environ[k] = v
    else:
        logging.warning("no secrets file found!")


# https://stackoverflow.com/questions/55179786/is-it-possible-to-provide-secret-to-docker-run
# https://spacelift.io/blog/docker-secrets
# https://towardsdatascience.com/secure-your-docker-images-with-docker-secrets-f2b92ec398a0
