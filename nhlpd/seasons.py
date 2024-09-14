from datetime import datetime
import pandas as pd
from .api_query import fetch_json_data
from .mysql_db import db_import_login
from .teams import TeamsImport
from .import_table_update_log import ImportTableUpdateLog


class SeasonsImport:
    seasons_df = pd.DataFrame(columns=['triCode', 'seasonId'])

    def __init__(self, seasons_df=pd.DataFrame()):
        self.seasons_df = pd.concat([self.seasons_df, seasons_df])

    def updateDB(self, tri_code=''):
        if len(self.seasons_df) > 0:
            cursor, db = db_import_login()

            if tri_code != '':
                self.seasons_df = self.seasons_df[self.seasons_df['triCode'] == tri_code]

            for index, row in self.seasons_df.iterrows():
                sql = "insert into team_seasons_import (triCode, seasonId) values (%s, %s)"
                val = (row['triCode'], row['seasonId'])
                cursor.execute(sql, val)

            db.commit()
            cursor.close()
            db.close()

        log_object = ImportTableUpdateLog("team_seasons_import", datetime.today().strftime('%Y-%m-%d %H:%M:%S'), 1)
        log_object.updateDB()

        return True

    @staticmethod
    def clearDB(tri_code):
        cursor, db = db_import_login()

        if tri_code == '':
            sql = "truncate table team_seasons_import"
        else:
            sql = "delete from team_seasons_import where triCode = " + tri_code

        cursor.execute(sql)

        db.commit()
        cursor.close()
        db.close()
        return True

    def queryDB(self, tri_code=''):
        sql_prefix = "select triCode, seasonId from team_seasons_import"
        sql_suffix = ""

        if tri_code != '':
            sql_suffix = " where triCode = " + tri_code

        sql = "{}{}".format(sql_prefix, sql_suffix)

        cursor, db = db_import_login()
        seasons_df = pd.read_sql(sql, db)
        self.seasons_df = seasons_df.fillna('')

        db.commit()
        cursor.close()
        db.close()

        return True

    def queryNHL(self, tri_code=''):
        teams = TeamsImport()
        teams.queryDB()

        team_seasons_df = pd.DataFrame()

        for index, row in teams.teams_df.iterrows():
            base_url = 'https://api-web.nhle.com/v1/roster-season/'
            query_string = "{}{}".format(base_url, row['triCode'])
            json_data = fetch_json_data(query_string)

            seasons_df = pd.DataFrame(json_data)
            seasons_df.rename(columns={0: "seasonId"}, inplace=True)
            seasons_df['triCode'] = row['triCode']

            team_seasons_df = pd.concat([team_seasons_df, seasons_df])

        self.seasons_df = team_seasons_df

        if tri_code != '':
            self.seasons_df = self.seasons_df[self.seasons_df['triCode'] == tri_code]

        return True

    def queryNHLupdateDB(self, tri_code=''):
        self.queryNHL(tri_code)
        self.clearDB(tri_code)
        self.updateDB(tri_code)

        return True
