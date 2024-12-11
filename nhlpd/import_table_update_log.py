from datetime import datetime
import pandas as pd
from .mysql_db import db_import_login


class ImportTableUpdateLog:
    update_details = pd.Series(index=['tableName', 'lastDateUpdated', 'updateFound'])

    def __init__(self):
        self.update_details = pd.concat([self.update_details, self.queryDB()])

    @staticmethod
    def updateDB(table_name, update_found=1):
        cursor, db = db_import_login()

        sql = "insert into table_update_log (tableName, lastDateUpdated, updateFound) values (%s, %s, %s)"
        val = (table_name, datetime.now(), update_found)
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

        db.commit()
        cursor.close()
        db.close()

        return update_details

    def lastUpdate(self, table_name):
        return self.update_details.loc[self.update_details['tableName'] == table_name, 'lastDateUpdated'].item()
