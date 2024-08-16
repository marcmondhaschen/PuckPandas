import os
import mysql.connector
from dotenv import load_dotenv


def db_import_login():
    """
    Uses dotenv library and local .env credentials to provide database access to the import schema

    Parameters:

    Returns: Database cursor and reference objects
    """
    load_dotenv()

    db = mysql.connector.connect(
        host=os.environ['DB_IMPORT_HOST'],
        user=os.environ['DB_IMPORT_USER'],
        password=os.environ['DB_IMPORT_PASSWORD'],
        database=os.environ['DB_IMPORT_SCHEMA']
    )

    cursor = db.cursor()

    return cursor, db



def db_test_login():
    """
    Uses dotenv library and local .env credentials to provide database access to the test schema

    Parameters:

    Returns: Database cursor and reference objects
    """
    load_dotenv()

    db = mysql.connector.connect(
        host=os.environ['DB_TEST_HOST'],
        user=os.environ['DB_TEST_USER'],
        password=os.environ['DB_TEST_PASSWORD'],
        database=os.environ['DB_TEST_SCHEMA']
    )

    cursor = db.cursor()

    return cursor, db
