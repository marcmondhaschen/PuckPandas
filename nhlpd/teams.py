import pandas as pd
import nhlpd
from sqlalchemy import text

class TeamsImport:
    def __init__(self):
        self.teams_df = self.query_db()
        self.table_columns = ['teamId', 'franchiseId', 'fullName', 'leagueId', 'triCode']

    def update_db(self, tri_code=''):
        if len(self.teams_df.index) > 0:
            if tri_code != '':
                self.teams_df = self.teams_df[self.teams_df['triCode'] == tri_code]

            engine = nhlpd.dba_import_login()
            sql = "insert into teams_import (teamId, franchiseId, fullName, leagueId, triCode) values (:teamId, " \
                  ":franchiseId, :fullName, :leagueId, :triCode)"
            params = self.teams_df.to_dict('records')
            with engine.connect() as conn:
                conn.execute(text(sql), parameters=params)

        return True

    @staticmethod
    def clear_db(tri_code=''):
        engine = nhlpd.dba_import_login()
        if tri_code == '':
            sql = "truncate table teams_import"
        else:
            sql = "delete from teams_import where triCode = '" + tri_code + "'"
        with engine.connect() as conn:
            conn.execute(text(sql))
        engine.dispose()

        return True

    @staticmethod
    def query_db(tri_code=''):
        engine = nhlpd.dba_import_login()
        sql_prefix = "select teamId, franchiseId, fullName, leagueId, triCode from teams_import "
        sql_suffix = ""
        if tri_code != '':
            sql_suffix = "where triCode = " + tri_code
        sql = "{}{}".format(sql_prefix, sql_suffix)
        teams_df = pd.read_sql_query(sql, engine)
        engine.dispose()

        return teams_df

    def query_nhl(self, tri_code=''):
        json_data = nhlpd.fetch_json_data('https://api.nhle.com/stats/rest/en/team')
        if json_data != {}:
            teams_df = pd.json_normalize(json_data, record_path=['data'])
            teams_df.rename(columns={'id': 'teamId'}, inplace=True)
            teams_df = teams_df.reindex(columns=self.table_columns)
            teams_df.fillna(0, inplace=True)
            self.teams_df = teams_df

        if tri_code != '':
            self.teams_df = self.teams_df[self.teams_df['triCode'] == tri_code]

        return True

    def query_nhl_update_db(self, tri_code=''):
        self.query_nhl(tri_code)
        self.clear_db(tri_code)
        self.update_db(tri_code)

        return True

    def team_id_from_tri_code(self, tri_code):
        team_id = self.teams_df.loc[self.teams_df['triCode'] == tri_code, 'teamId'].item()

        return team_id

    def tri_code_from_team_id(self, team_id):
        tri_code = self.teams_df.loc[self.teams_df['teamId'] == team_id, 'triCode'].item()

        return tri_code
