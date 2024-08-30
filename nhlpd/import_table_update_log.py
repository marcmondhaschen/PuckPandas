import pandas as pd
from .mysql_db import db_import_login


class ImportTableUpdateLog:
    update_details = pd.Series(index=['tableName', 'lastDateUpdated', 'updateFound'])

    def __init__(self, table_name="", last_date_updated="", update_found=0):
        self.update_details['tableName'] = table_name
        self.update_details['lastDateUpdated'] = last_date_updated
        self.update_details['updateFound'] = update_found

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

    @staticmethod
    def queryDB(table_name='', update_found=1):
        cursor, db = db_import_login()

        prefix_sql = "select tableName, max(lastDateUpdated) as lastDateUpdated, " \
                     "updateFound from table_update_log where tableName = '"
        suffix_sql = "' and updateFound = "
        suffix2_sql = " group by tableName, updateFound"
        update_log_sql = "{}{}{}{}{}".format(prefix_sql, table_name, suffix_sql, update_found, suffix2_sql)
        update_df = pd.read_sql(update_log_sql, db)
        last_update_date = update_df.iloc[0]["lastDateUpdated"]

        db.commit()
        cursor.close()
        db.close()

        return last_update_date
