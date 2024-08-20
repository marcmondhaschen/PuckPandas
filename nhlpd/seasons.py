import pandas as pd
from .api_query import fetch_json_data
from .mysql_db import db_import_login
from .teams import TeamsImport


class SeasonsImport:
    seasons_df = pd.DataFrame(columns=['triCode', 'seasonId'])

    def __init__(self, seasons_df=pd.DataFrame()):
        self.seasons_df = pd.concat([self.seasons_df, seasons_df])

    @staticmethod
    def updateDB(self):
        if len(self.seasons_df) > 0:
            cursor, db = db_import_login()

            for index, row in self.seasons_df.iterrows():
                sql = "insert into team_seasons_import (triCode, seasonId) values (%s, %s)"
                val = (row['triCode'], row['seasonId'])
                cursor.execute(sql, val)

            db.commit()
            cursor.close()
            db.close()

        return True

    @staticmethod
    def clearDB():
        cursor, db = db_import_login()

        sql = "truncate table team_seasons_import"
        cursor.execute(sql)

        db.commit()
        cursor.close()
        db.close()
        return True

    def queryDB(self):
        seasons_sql = "select triCode, seasonId from team_seasons_import"

        cursor, db = db_import_login()
        seasons_df = pd.read_sql(seasons_sql, db)
        self.seasons_df = seasons_df.fillna('')

        return True

    def queryNHL(self):
        cursor, db = db_import_login()

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

            self.seasons_df = pd.concat([self.seasons_df, seasons_df])

        self.seasons_df = team_seasons_df

        # tidy up the cursors
        db.commit()
        cursor.close()
        db.close()

    def queryNHLupdateDB(self):
        self.queryNHL()
        self.clearDB()
        self.updateDB(self)

        return True
