import pandas as pd
import nhlpd
from sqlalchemy import text


class SeasonsImport:
    def __init__(self):
        self.seasons_df = self.query_db()

    def update_db(self, tri_code=''):
        if self.seasons_df.size > 0:
            if tri_code != '':
                self.seasons_df = self.seasons_df[self.seasons_df['triCode'] == tri_code]

            engine = nhlpd.dba_import_login()
            sql = "insert into team_seasons_import (triCode, seasonId) values (:triCode, :seasonId)"
            params = self.seasons_df.to_dict('records')
            with engine.connect() as conn:
                conn.execute(text(sql), parameters=params)

        return True

    @staticmethod
    def clear_db(tri_code):
        engine = nhlpd.dba_import_login()
        if tri_code == '':
            sql = "truncate table team_seasons_import"
        else:
            sql = "delete from team_seasons_import where triCode = " + tri_code
        with engine.connect() as conn:
            conn.execute(text(sql))
        engine.dispose()

        return True

    @staticmethod
    def query_db(tri_code='', season_id=''):
        engine = nhlpd.dba_import_login()
        sql_prefix = "select a.triCode, b.teamId, a.seasonId from team_seasons_import as a join teams_import as b " \
                     "on a.triCode = b.triCode where b.teamId is not null"
        sql_suffix = ""
        if tri_code != '':
            sql_suffix += " and a.triCode = " + tri_code
        if season_id != '':
            sql_suffix += " and a.seasonId = " + season_id
        sql = "{}{}".format(sql_prefix, sql_suffix)
        seasons_df = pd.read_sql_query(sql, engine)
        engine.dispose()

        seasons_df.fillna('', inplace=True)

        return seasons_df

    def query_nhl(self, tri_code=''):
        teams = nhlpd.TeamsImport()
        teams.query_db()

        team_seasons_df = pd.DataFrame()

        for index, row in teams.teams_df.iterrows():
            base_url = 'https://api-web.nhle.com/v1/roster-season/'
            query_string = "{}{}".format(base_url, row['triCode'])
            json_data = nhlpd.fetch_json_data(query_string)

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
