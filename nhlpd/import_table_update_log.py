import pandas as pd
from .mysql_db import db_import_login


class ImportTableUpdateLog:
    table_update_log = pd.DataFrame(columns=['tableName', 'lastDateUpdated', 'updateFound'])

    def __init__(self, table_update_log=pd.DataFrame()):
        self.table_update_log = pd.concat([self.table_update_log, table_update_log])

    @staticmethod
    def updateDB(self):
        if (len(self.table_update_log) > 0) and ('tableName' in self.table_update_log):
            cursor, db = db_import_login()

            for index, row in self.table_update_log.iterrows():
                sql = "insert into table_update_log (tableName, lastDateUpdated, updateFound) values (%s, %s, %s)"
                val = (row['tableName'], row['lastDateUpdated'], row['updateFound'])
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

        self.table_update_log = pd.read_sql(update_log_sql, db)
        self.table_update_log.fillna('', inplace=True)

        db.commit()
        cursor.close()
        db.close()

        return True
