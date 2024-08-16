import os
import mysql.connector
from dotenv import load_dotenv


def db_login():
    """
    Uses dotenv library and local .env credentials to provide database access

    Parameters:

    Returns: Database cursor and reference objects
    """
    load_dotenv()

    db = mysql.connector.connect(
        host=os.environ['DB_HOST'],
        user=os.environ['DB_USER'],
        password=os.environ['DB_PASSWORD'],
        database=os.environ['DB_SCHEMA']
    )

    cursor = db.cursor()

    return cursor, db
