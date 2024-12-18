from datetime import datetime, timezone
import pandas as pd
from .mysql_db import db_import_login


class ImportTableUpdateLog:
    update_details = pd.DataFrame(columns=['tableName', 'lastDateUpdated', 'updateFound'])

    def __init__(self):
        self.update_details = pd.concat([self.update_details, self.queryDB()])

    @staticmethod
    def updateDB(table_name, update_found=1):
        cursor, db = db_import_login()

        sql = "insert into table_update_log (tableName, lastDateUpdated, updateFound) values (%s, %s, %s)"
        val = (table_name, datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S'), update_found)
        cursor.execute(sql, val)

        db.commit()
        cursor.close()
        db.close()

        return True

    @staticmethod
    def queryDB():
        cursor, db = db_import_login()

        sql = "select tableName, max(lastDateUpdated) as lastDateUpdated from table_update_log group by tableName"
        update_details = pd.read_sql(sql, db)
        update_details.fillna('', inplace=True)

        db.commit()
        cursor.close()
        db.close()

        return update_details

    def lastUpdate(self, table_name):
        last_update = None

        update_exists = self.update_details['tableName'].isin([table_name]).any()

        if update_exists:
            last_update = self.update_details.loc[self.update_details['tableName'] == table_name,
                                                  'lastDateUpdated'].values[0]

        return last_update
