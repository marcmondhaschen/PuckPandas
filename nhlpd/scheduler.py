from datetime import datetime
import pandas as pd
from .api_query import fetch_json_data
from .mysql_db import db_import_login


class Scheduler:
    def __init__(self):
        self.current_time = datetime.now()
