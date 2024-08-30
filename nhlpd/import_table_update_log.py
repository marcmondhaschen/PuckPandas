import pandas as pd
from .mysql_db import db_import_login


class ImportTableUpdateLog:
    update_details = pd.Series(index=['tableName', 'lastDateUpdated', 'updateFound'])

    def __init__(self, update_details=pd.Series(index=['tableName', 'lastDateUpdated', 'updateFound'])):
        self.update_details = update_details

    @staticmethod
    def updateDB(self):
        if (len(self.update_details) > 0) and ('tableName' in self.update_details):
            cursor, db = db_import_login()

            sql = "insert into table_update_log (tableName, lastDateUpdated, updateFound) values (%s, %s, %s)"
            val = (self.update_details['tableName'], self.update_details['lastDateUpdated'],
                   self.update_details['updateFound'])
            cursor.execute(sql, val)

            db.commit()
            cursor.close()
            db.close()

        return True

    def queryDB(self, table_name='', update_found=1):
        cursor, db = db_import_login()

        prefix_sql = "select tableName, max(lastDateUpdated) as lastDateUpdated, " \
                     "updateFound from table_update_log where tableName = '"
        suffix_sql = "' and updateFound = "
        suffix2_sql = " group by tableName, updateFound"
        update_log_sql = "{}{}{}{}{}".format(prefix_sql, table_name, suffix_sql, update_found, suffix2_sql)

        self.update_details = pd.read_sql(update_log_sql, db)
        self.update_details.fillna('', inplace=True)

        db.commit()
        cursor.close()
        db.close()

        return True
