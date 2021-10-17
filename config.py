from os import environ

"""
Parametros de configuracion para ejecucion de aplicacion
"""

FLASK_ENV = 'development'
DB_URL = 'mysql://user:password@localhost/webscraping'
SECRET_KEY = 'Cn<?&8v2"HPa,@mh'


def get_config():
    """

    :return:
    """
    enviroment = FLASK_ENV
    if enviroment == 'development':
        return Development
    return Production


class Development:
    SQLALCHEMY_DATABASE_URI = DB_URL
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = SECRET_KEY


class Production:
    SQLALCHEMY_DATABASE_URI = DB_URL
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = SECRET_KEY
