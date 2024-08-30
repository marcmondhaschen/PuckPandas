from datetime import datetime
import pandas as pd
from .api_query import fetch_json_data
from .mysql_db import db_import_login
from .import_table_update_log import ImportTableUpdateLog


class TeamsImport:
    teams_df = pd.DataFrame(columns=['id', 'franchiseId', 'fullName', 'leagueId', 'rawTricode', 'triCode'])

    def __init__(self, teams_df=pd.DataFrame()):
        self.teams_df = pd.concat([self.teams_df, teams_df])

    @staticmethod
    def updateDB(self):
        cursor, db = db_import_login()

        if len(self.teams_df) > 0:
            for index, row in self.teams_df.iterrows():
                sql = "insert into teams_import (teamId, franchiseId, fullName, leagueId, triCode) " \
                      "values (%s, %s, %s, %s, %s)"
                val = (row['id'], row['franchiseId'], row['fullName'], row['leagueId'], row['triCode'])
                cursor.execute(sql, val)

        log_object = ImportTableUpdateLog("teams_import", datetime.today().strftime('%Y-%m-%d %H:%M:%S'), 1)
        log_object.updateDB(log_object)

        db.commit()
        cursor.close()
        db.close()
        return True

    @staticmethod
    def clearDB():
        cursor, db = db_import_login()

        sql = "truncate table teams_import"
        cursor.execute(sql)

        db.commit()
        cursor.close()
        db.close()
        return True

    def queryDB(self):
        teams_sql = "select teamId, franchiseId, fullName, leagueId, triCode from teams_import"

        cursor, db = db_import_login()
        teams_df = pd.read_sql(teams_sql, db)
        self.teams_df = teams_df.fillna('')

        db.commit()
        cursor.close()
        db.close()

        return True

    def queryNHL(self):
        json_data = fetch_json_data('https://api.nhle.com/stats/rest/en/team')
        api_teams_df = pd.json_normalize(json_data, record_path=['data'])
        api_teams_df = api_teams_df.fillna('')
        self.teams_df = pd.concat([self.teams_df, api_teams_df])

        return True

    def queryNHLupdateDB(self):
        self.queryNHL()
        self.clearDB()
        self.updateDB(self)

        return True
