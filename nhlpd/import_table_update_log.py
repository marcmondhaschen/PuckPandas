from datetime import datetime, timezone
import numpy as np
import pandas as pd
import nhlpd
from sqlalchemy import text


class ImportTableUpdateLog:
    def __init__(self):
        self.update_details = self.query_db()
        self.update_details = self.update_details.reindex(columns=['tableName', 'lastDateUpdated'])

    @staticmethod
    def update_db(table_name, update_found=1):
        engine = nhlpd.dba_import_login()
        sql = "insert into table_update_log (tableName, lastDateUpdated, updateFound) values " \
              "(:tableName, :lastDateUpdated, :updateFound)"
        param = {'tableName': table_name,
                 'lastDateUpdated': np.datetime64(datetime.now(timezone.utc).replace(tzinfo=None)).astype(str),
                 'updateFound': update_found}
        with engine.connect() as conn:
            conn.execute(text(sql), parameters=param)

        return True

    @staticmethod
    def query_db():
        engine = nhlpd.dba_import_login()
        sql = "select tableName, max(lastDateUpdated) as lastDateUpdated from table_update_log group by tableName"
        update_details = pd.read_sql_query(sql, engine)
        engine.dispose()

        if update_details.size > 0:
            update_details.fillna('', inplace=True)

        return update_details

    def last_update(self, table_name):
        last_update = None

        update_exists = self.update_details['tableName'].isin([table_name]).any()

        if update_exists:
            last_update = self.update_details.loc[self.update_details['tableName'] == table_name,
                                                  'lastDateUpdated'].values[0]

        return last_update
