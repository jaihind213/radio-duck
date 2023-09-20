import configparser

app_config = configparser.SafeConfigParser()


def setup_app_config(default_ini):
    with open(default_ini) as cf:
        app_config.read_file(cf)


def get_config():
    return app_config
