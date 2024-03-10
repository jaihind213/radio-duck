import configparser
import logging
import os

app_config = configparser.SafeConfigParser()


def setup_app_config(default_ini):
    with open(default_ini) as cf:
        app_config.read_file(cf)


def get_config():
    return app_config


# https://stackoverflow.com/questions/55179786/is-it-possible-to-provide-secret-to-docker-run
# https://spacelift.io/blog/docker-secrets
# https://towardsdatascience.com/secure-your-docker-images-with-docker-secrets-f2b92ec398a0
