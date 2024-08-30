from datetime import datetime
import pandas as pd
from .api_query import fetch_json_data
from .mysql_db import db_import_login
from .seasons import SeasonsImport
from .import_table_update_log import ImportTableUpdateLog


class RostersImport:
    rosters_df = pd.DataFrame(columns=['triCode', 'seasonId', 'playerId'])

    def __init__(self, rosters_df=pd.DataFrame()):
        self.rosters_df = pd.concat([self.rosters_df, rosters_df])

    @staticmethod
    def updateDB(self):
        if len(self.rosters_df) > 0:
            cursor, db = db_import_login()

            for index, row in self.rosters_df.iterrows():
                if 'id' in row:
                    sql = "insert into rosters_import (triCode, seasonId, playerId) " \
                          "values (%s, %s, %s)"
                    val = (row['triCode'], row['seasonId'], row['id'])
                    cursor.execute(sql, val)

            db.commit()
            cursor.close()
            db.close()

        update_details = pd.Series(index=['tableName', 'lastDateUpdated', 'updateFound'])
        update_details['tableName'] = "rosters_import"
        update_details['lastDateUpdated'] = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
        update_details['updateFound'] = 1
        log_object = ImportTableUpdateLog(update_details)
        log_object.updateDB(log_object)

        return True

    @staticmethod
    def clearDB():
        cursor, db = db_import_login()

        sql = "truncate table rosters_import"
        cursor.execute(sql)

        db.commit()
        cursor.close()
        db.close()
        return True

    def queryDB(self):
        rosters_sql = "select triCode, seasonId, playerId from rosters_import"

        cursor, db = db_import_login()
        rosters_df = pd.read_sql(rosters_sql, db)
        self.rosters_df = rosters_df.fillna('')

        return True

    def queryNHL(self):
        cursor, db = db_import_login()

        seasons = SeasonsImport()
        seasons.queryDB()

        db.commit()
        cursor.close()
        db.close()

        rosters_df = pd.DataFrame()

        for index, row in seasons.seasons_df.iterrows():
            url_prefix = "https://api-web.nhle.com/v1/roster/"
            query_url = "{}{}/{}".format(url_prefix, row['triCode'], row['seasonId'])

            json_data = fetch_json_data(query_url)

            forwards_data = pd.json_normalize(json_data, record_path=['forwards'])
            defensemen_data = pd.json_normalize(json_data, record_path=['defensemen'])
            goalies_data = pd.json_normalize(json_data, record_path=['goalies'])

            this_roster_df = pd.concat([forwards_data, defensemen_data, goalies_data])
            # this_roster_df = this_roster_df[['id']]
            this_roster_df['triCode'] = row['triCode']
            this_roster_df['seasonId'] = row['seasonId']
            this_roster_df.fillna('', inplace=True)
            rosters_df = pd.concat([rosters_df, this_roster_df])

        self.rosters_df = rosters_df

        return True

    def queryNHLupdateDB(self):
        self.queryNHL()
        self.clearDB()
        self.updateDB(self)
        return True
