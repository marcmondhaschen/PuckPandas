import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, NullPool


def dba_import_login(test=0):
    load_dotenv()
    dialect = "mysql"
    driver = "mysqlconnector"

    if test == 0:
        server = os.environ['DB_IMP_HOST']
        port = os.environ['DB_IMP_PORT']
        schema = os.environ['DB_IMP_SCHEMA']
        username = os.environ['DB_IMP_USER']
        password = os.environ['DB_IMP_PASSWORD']
    else:
        server = os.environ['DB_IMP_TEST_HOST']
        port = os.environ['DB_IMP_TEST_PORT']
        schema = os.environ['DB_IMP_TEST_SCHEMA']
        username = os.environ['DB_IMP_TEST_USER']
        password = os.environ['DB_IMP_TEST_PASSWORD']

    connection_string = "{}+{}://{}:{}@{}:{}/{}?charset=utf8mb4".format(dialect, driver, username, password,
                                                                        server, port, schema)
    engine = create_engine(connection_string, poolclass=NullPool)

    return engine

def dba_prod_tx(test=0):
    load_dotenv()
    dialect = "mysql"
    driver = "mysqlconnector"

    if test == 0:
        server = os.environ['DB_TX_HOST']
        port = os.environ['DB_TX_PORT']
        schema = os.environ['DB_TX_SCHEMA']
        username = os.environ['DB_TX_USER']
        password = os.environ['DB_TX_PASSWORD']
    else:
        server = os.environ['DB_TX_TEST_HOST']
        port = os.environ['DB_TX_TEST_PORT']
        schema = os.environ['DB_TX_TEST_SCHEMA']
        username = os.environ['DB_TX_TEST_USER']
        password = os.environ['DB_TX_TEST_PASSWORD']

    connection_string = "{}+{}://{}:{}@{}:{}/{}?charset=utf8mb4".format(dialect, driver, username, password,
                                                                        server, port, schema)
    engine = create_engine(connection_string, poolclass=NullPool)

    return engine

def dba_prod_login(test=0):
    load_dotenv()
    dialect = "mysql"
    driver = "mysqlconnector"

    if test == 0:
        server = os.environ['DB_PROD_HOST']
        port = os.environ['DB_PROD_PORT']
        schema = os.environ['DB_PROD_SCHEMA']
        username = os.environ['DB_PROD_USER']
        password = os.environ['DB_PROD_PASSWORD']
    else:
        server = os.environ['DB_PROD_TEST_HOST']
        port = os.environ['DB_PROD_TEST_PORT']
        schema = os.environ['DB_PROD_TEST_SCHEMA']
        username = os.environ['DB_PROD_TEST_USER']
        password = os.environ['DB_PROD_TEST_PASSWORD']

    connection_string = "{}+{}://{}:{}@{}:{}/{}?charset=utf8mb4".format(dialect, driver, username, password,
                                                                        server, port, schema)
    engine = create_engine(connection_string)

    return engine

def db_ana_login():
    load_dotenv()
    dialect = "mysql"
    driver = "mysqlconnector"

    server = os.environ['DB_ANA_HOST']
    port = os.environ['DB_ANA_PORT']
    schema = os.environ['DB_ANA_SCHEMA']
    username = os.environ['DB_ANA_USER']
    password = os.environ['DB_ANA_PASSWORD']

    connection_string = "{}+{}://{}:{}@{}:{}/{}?charset=utf8mb4".format(dialect, driver, username, password,
                                                                        server, port, schema)
    engine = create_engine(connection_string)

    return engine
