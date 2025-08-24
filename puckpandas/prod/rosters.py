import pandas as pd
import puckpandas
from sqlalchemy import text


class RostersImport:
    def __init__(self, team_id, season_id):
        self.team_id = team_id
        self.season_id = season_id
        self.teams = puckpandas.TeamsImport()
        self.tri_code = self.teams.tri_code_from_team_id(self.team_id)
        self.table_columns = ['triCode', 'seasonId', 'playerId']
        self.roster_df = pd.DataFrame()
        self.query_db()

    def update_db(self):
        if self.roster_df.size > 0:
            engine = puckpandas.dba_import_login()
            sql = "insert into puckpandas_import.rosters_import (triCode, seasonId, playerId) " \
                  "values (:triCode, :seasonId, :playerId)"
            params = self.roster_df.to_dict('records')
            with engine.connect() as conn:
                conn.execute(text(sql), parameters=params)

        return True

    def clear_db(self):
        if self.tri_code != '' and self.season_id != '':
            engine = puckpandas.dba_import_login()
            sql = "delete from puckpandas_import.rosters_import where triCode = '" + str(self.tri_code) + "' and " \
                  "seasonId = " + str(self.season_id)
            with engine.connect() as conn:
                conn.execute(text(sql))

        return True

    def query_db(self):
        engine = puckpandas.dba_import_login()
        sql = "select triCode, seasonId, playerId from puckpandas_import.rosters_import where seasonId > 0 and " \
              "triCode = '" + str(self.tri_code) + "' and seasonId = '" + str(self.season_id) + "'"
        roster_df = pd.read_sql_query(sql, engine)
        engine.dispose()

        if roster_df.size > 0:
            roster_df.infer_objects().fillna('', inplace=True)
            self.roster_df = roster_df

        return self.roster_df

    def query_api(self):
        base_url = 'https://api-web.nhle.com/v1/roster/'
        query_string = "{}{}/{}".format(base_url, self.tri_code, self.season_id)
        json_data = puckpandas.fetch_json_data(query_string)

        if len(json_data['forwards']) > 0:
            forwards_data = pd.json_normalize(json_data, record_path=['forwards'])
            defensemen_data = pd.json_normalize(json_data, record_path=['defensemen'])
            goalies_data = pd.json_normalize(json_data, record_path=['goalies'])
            roster_df = pd.concat([forwards_data, defensemen_data, goalies_data])

            if 'id' in roster_df:
                roster_df.rename(columns={"id": "playerId"}, inplace=True)
                roster_df = roster_df[['playerId']]
                roster_df['triCode'] = self.tri_code
                roster_df['seasonId'] = self.season_id
                self.roster_df = roster_df

        self.roster_df = self.roster_df.reindex(columns=self.table_columns)

        return self.roster_df

    def query_api_update_db(self):
        self.query_api()
        self.clear_db()
        self.update_db()
        return True
