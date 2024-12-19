import pandas as pd
from .api_query import fetch_json_data
from .mysql_db import db_import_login
from .teams import TeamsImport


class SeasonsImport:
    def __init__(self):
        self.seasons_df = self.query_db()

    def update_db(self, tri_code=''):
        if not self.seasons_df.empty:
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

        return True

    @staticmethod
    def clear_db(tri_code):
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

    @staticmethod
    def query_db(tri_code='', season_id=''):
        sql_prefix = "select a.triCode, b.teamId, a.seasonId from team_seasons_import as a join teams_import as b " \
                     "on a.triCode = b.triCode where b.teamId is not null"
        sql_suffix = ""
        if tri_code != '':
            sql_suffix += " and a.triCode = " + tri_code
        if season_id != '':
            sql_suffix += " and a.seasonId = " + season_id
        sql = "{}{}".format(sql_prefix, sql_suffix)

        cursor, db = db_import_login()
        seasons_df = pd.read_sql(sql, db)
        db.commit()
        cursor.close()
        db.close()

        seasons_df = seasons_df.fillna('')

        return seasons_df

    def query_nhl(self, tri_code=''):
        teams = TeamsImport()
        teams.query_db()

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

    def query_nhl_update_db(self, tri_code=''):
        self.query_nhl(tri_code)
        self.clear_db(tri_code)
        self.update_db(tri_code)

        return True
