import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, NullPool

def dba_import_login():
    load_dotenv()

    dialect = "mysql"
    driver = "mysqlconnector"
    username = os.environ['DB_IMPORT_USER']
    password = os.environ['DB_IMPORT_PASSWORD']
    server = os.environ['DB_IMPORT_HOST']
    port = os.environ['DB_IMPORT_PORT']
    schema = os.environ['DB_IMPORT_SCHEMA']

    connection_string = "{}+{}://{}:{}@{}:{}/{}?charset=utf8mb4".format(dialect, driver, username, password,
                                                                        server, port, schema)
    engine = create_engine(connection_string, poolclass=NullPool)

    return engine


def dba_test_login():
    load_dotenv()

    dialect = "mysql"
    driver = "mysqlconnector"
    username = os.environ['DB_TEST_USER']
    password = os.environ['DB_TEST_PASSWORD']
    server = os.environ['DB_TEST_HOST']
    port = os.environ['DB_TEST_PORT']
    schema = os.environ['DB_TEST_SCHEMA']

    connection_string = "{}+{}://{}:{}@{}:{}/{}?charset=utf8mb4".format(dialect, driver, username, password,
                                                                        server, port, schema)
    engine = create_engine(connection_string)

    return engine

def db_prod_tx_login():
    load_dotenv()

    dialect = "mysql"
    driver = "mysqlconnector"
    username = os.environ['DB_PROD_TX_USER']
    password = os.environ['DB_PROD_TX_PASSWORD']
    server = os.environ['DB_PROD_TX_HOST']
    port = os.environ['DB_PROD_TX_PORT']
    schema = os.environ['DB_PROD_TX_SCHEMA']

    connection_string = "{}+{}://{}:{}@{}:{}/{}?charset=utf8mb4".format(dialect, driver, username, password,
                                                                        server, port, schema)
    engine = create_engine(connection_string)

    return engine

def db_prod_login():
    load_dotenv()

    dialect = "mysql"
    driver = "mysqlconnector"
    username = os.environ['DB_PROD_USER']
    password = os.environ['DB_PROD_PASSWORD']
    server = os.environ['DB_PROD_HOST']
    port = os.environ['DB_PROD_PORT']
    schema = os.environ['DB_PROD_SCHEMA']

    connection_string = "{}+{}://{}:{}@{}:{}/{}?charset=utf8mb4".format(dialect, driver, username, password,
                                                                        server, port, schema)
    engine = create_engine(connection_string)

    return engine

