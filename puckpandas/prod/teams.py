import pandas as pd
import puckpandas
from sqlalchemy import text

class TeamsImport:
    def __init__(self, test=0):
        self.test = test
        self.table_columns = ['teamId', 'franchiseId', 'fullName', 'leagueId', 'triCode']
        self.teams_df = self.query_db()
        self.teams_df = self.teams_df.reindex(columns=self.table_columns)

    def update_db(self, tri_code=''):
        if len(self.teams_df.index) > 0:
            if tri_code != '':
                self.teams_df = self.teams_df[self.teams_df['triCode'] == tri_code]

            engine = puckpandas.dba_import_login(test=self.test)

            sql = "insert into puckpandas_import.teams_import (teamId, franchiseId, fullName, leagueId, triCode) " \
                  "values (:teamId, :franchiseId, :fullName, :leagueId, :triCode)"
            params = self.teams_df.to_dict('records')
            with engine.connect() as conn:
                conn.execute(text(sql), parameters=params)

            # self.teams_df.to_sql(name='teams_import', con=engine, schema='puckpandas_import', if_exists='replace',
            #                      index=False)

        return True

    def clear_db(self, tri_code=''):
        engine = puckpandas.dba_import_login(test=self.test)
        if tri_code == '':
            sql = "truncate table puckpandas_import.teams_import"
        else:
            sql = "delete from puckpandas_import.teams_import where triCode = '" + tri_code + "'"
        with engine.connect() as conn:
            conn.execute(text(sql))
        engine.dispose()

        return True

    def query_db(self, tri_code=''):
        engine = puckpandas.dba_import_login(test=self.test)
        sql_prefix = "select teamId, franchiseId, fullName, leagueId, triCode from puckpandas_import.teams_import "
        sql_suffix = ""
        if tri_code != '':
            sql_suffix = "where triCode = " + tri_code
        sql = "{}{}".format(sql_prefix, sql_suffix)
        teams_df = pd.read_sql_query(sql, engine)
        engine.dispose()

        return teams_df

    def query_api(self, tri_code=''):
        json_data = puckpandas.fetch_json_data('https://api.nhle.com/stats/rest/en/team')
        if json_data != {}:
            teams_df = pd.json_normalize(json_data, record_path=['data'])
            teams_df.rename(columns={'id': 'teamId'}, inplace=True)
            teams_df = teams_df.reindex(columns=self.table_columns)
            teams_df.fillna(0, inplace=True)
            self.teams_df = teams_df

        if tri_code != '':
            self.teams_df = self.teams_df[self.teams_df['triCode'] == tri_code]

        return True

    def query_api_update_db(self, tri_code=''):
        self.query_api(tri_code)
        self.clear_db(tri_code)
        self.update_db(tri_code)

        return True

    def team_id_from_tri_code(self, tri_code):
        team_id = self.teams_df.loc[self.teams_df['triCode'] == tri_code, 'teamId'].item()

        return team_id

    def tri_code_from_team_id(self, team_id):
        tri_code = self.teams_df.loc[self.teams_df['teamId'] == team_id, 'triCode'].item()

        return tri_code
