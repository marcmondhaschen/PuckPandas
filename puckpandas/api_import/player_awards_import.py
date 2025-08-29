import pandas as pd
import puckpandas as pp
from sqlalchemy import text


class PlayerAwardsImport:
    def __init__(self, player_id):
        self.player_id = player_id
        self.json = {}
        self.table_columns = ['playerId', 'seasonId', 'trophy.default']
        self.player_awards_df = pd.DataFrame()
        self.player_awards_df = self.player_awards_df.reindex(columns=self.table_columns)

    def update_db(self):
        awards_found = 0
        if self.json != {}:
            awards_found = 1
            engine = pp.dba_import_login()
            sql = "insert into puckpandas_import.player_award_import (playerId, seasonId, `trophy.default`) values " \
                  "(:playerId, :seasonId, :trophydefault)"
            player_awards_transform_df = self.player_awards_df
            player_awards_transform_df.columns = player_awards_transform_df.columns.str.replace('.', '')
            params = player_awards_transform_df.to_dict('records')

            with engine.connect() as conn:
                conn.execute(text(sql), parameters=params)

        log = pp.PlayerImportLog(player_id=self.player_id, awards_found=awards_found)
        log.insert_db()

        return True

    def clear_db(self):
        engine = pp.dba_import_login()
        sql = "delete from puckpandas_import.player_award_import where playerId = " + str(self.player_id)
        with engine.connect() as conn:
            conn.execute(text(sql))
        engine.dispose()

        return True

    def query_db(self):
        engine = pp.dba_import_login()
        sql = "select playerId, gameTypeId, gamesPlayed, goalsAgainst, goalsAgainstAvg, leagueAbbrev, losses, " \
                     "season, sequence, shutouts, ties, timeOnIce, timeOnIceMinutes, timeOnIceSeconds, wins, " \
                     "`teamName.default`, savePctg, shotsAgainst, otLosses, assists, gamesStarted, goals, " \
                     "pim from puckpandas_import.goalie_season_import where playerId = " + str(self.player_id)
        player_awards_df = pd.read_sql_query(sql, engine)
        engine.dispose()

        if player_awards_df.size > 0:
            player_awards_df = player_awards_df.reindex(columns=self.table_columns)
            player_awards_df.fillna(0, inplace=True)
            self.player_awards_df = player_awards_df

        return True

    def query_api(self):
        player_awards_df = pd.json_normalize(self.json, record_path=["seasons"], meta=[["trophy", "default"]])
        player_awards_df.insert(0, 'playerId', self.player_id)

        if player_awards_df.size > 0:
            player_awards_df = player_awards_df.reindex(columns=self.table_columns)
            player_awards_df.infer_objects().fillna('', inplace=True)
            self.player_awards_df = player_awards_df

        return True

    def query_api_update_db(self):
        self.query_api()
        self.clear_db()
        self.update_db()

        return True
