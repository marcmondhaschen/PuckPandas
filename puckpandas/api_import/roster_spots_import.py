import pandas as pd
import puckpandas as pp
from sqlalchemy import text


class RosterSpotsImport:
    def __init__(self, game_id):
        self.game_id = game_id
        self.json = {}
        self.table_columns = ['gameId', 'teamId', 'playerId', 'sweaterNumber', 'positionCode', 'headshot',
                              'firstName.default', 'lastName.default']
        self.roster_spots_df = pd.DataFrame()
        self.query_db()
        self.roster_spots_df = self.roster_spots_df.reindex(columns=self.table_columns)

    def update_db(self):
        roster_spots_found = 0
        if self.roster_spots_df.size > 0:
            roster_spots_found = 1

            engine = pp.dba_import_login()
            sql = "insert into puckpandas_import.roster_spots_import (gameId, teamId, playerId, sweaterNumber, " \
                  "positionCode, headshot,`firstName`,`lastName`) values (:gameId, :teamId, :playerId, " \
                  ":sweaterNumber, :positionCode, :headshot, :firstNamedefault, :lastNamedefault)"
            roster_spots_df = self.roster_spots_df
            roster_spots_df.columns = roster_spots_df.columns.str.replace('.', '')
            roster_spots_df.fillna(0, inplace=True)
            params = roster_spots_df.to_dict('records')
            with engine.connect() as conn:
                conn.execute(text(sql), parameters=params)

        log = pp.GamesImportLog(game_id=self.game_id, roster_spots_found=roster_spots_found)
        log.insert_db()

        return True

    def clear_db(self):
        engine = pp.dba_import_login()
        sql = "delete from puckpandas_import.roster_spots_import where gameId = " + str(self.game_id)
        with engine.connect() as conn:
            conn.execute(text(sql))

        return True

    def query_db(self):
        engine = pp.dba_import_login()
        sql = "select gameId, teamId, playerId, sweaterNumber, positionCode, headshot, `firstName`, `lastName` from " \
              "puckpandas_import.roster_spots_import where gameId = " + str(self.game_id)
        roster_spots_df = pd.read_sql_query(sql, engine)
        engine.dispose()

        if roster_spots_df.size > 0:
            roster_spots_df = roster_spots_df.reindex(columns=self.table_columns)
            roster_spots_df.fillna(0, inplace=True)
            self.roster_spots_df = roster_spots_df

        return True

    def query_api(self):
        roster_spots_df = pd.json_normalize(self.json)
        roster_spots_df.insert(0, 'gameId', self.game_id)

        if roster_spots_df.size > 0:
            roster_spots_df = roster_spots_df.reindex(columns=self.table_columns)
            roster_spots_df.fillna(0, inplace=True)
            self.roster_spots_df = roster_spots_df

        return True

    def query_api_update_db(self):
        self.query_api()
        self.clear_db()
        self.update_db()

        return True
