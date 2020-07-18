ENV_VARS_MAP = {
    'RRT_TOKEN': '',
    'RRT_PERSISTENCE_PREFIX': '',
    'RRT_MYSQL_USER': '',
    'RRT_MYSQL_PWD': '',
    'RRT_MYSQL_DB': ''
}


def set_env_vars_map():
    from os import environ
    global ENV_VARS_MAP

    ENV_VARS_MAP['RRT_TOKEN'] = environ['RRT_TOKEN']
    ENV_VARS_MAP['RRT_PERSISTENCE_PREFIX'] = environ['RRT_PERSISTENCE_PREFIX']


def refresh_env_vars_map():
    set_env_vars_map()


def get_token():
    if 'RRT_TOKEN' not in ENV_VARS_MAP:
        set_env_vars_map()
    return ENV_VARS_MAP['RRT_TOKEN']


def get_persistence_filename_prefix():
    if 'RRT_PERSISTENCE_PREFIX' not in ENV_VARS_MAP:
        set_env_vars_map()
    return ENV_VARS_MAP['RRT_PERSISTENCE_PREFIX']


def get_mysql_username():
    if 'RRT_MYSQL_USER' not in ENV_VARS_MAP:
        set_env_vars_map()
    return ENV_VARS_MAP['RRT_MYSQL_USER']


def get_mysql_password():
    if 'RRT_MYSQL_PWD' not in ENV_VARS_MAP:
        set_env_vars_map()
    return ENV_VARS_MAP['RRT_MYSQL_PWD']


def get_mysql_db_name():
    if 'RRT_MYSQL_DB' not in ENV_VARS_MAP:
        set_env_vars_map()
    return ENV_VARS_MAP['RRT_MYSQL_DB']
