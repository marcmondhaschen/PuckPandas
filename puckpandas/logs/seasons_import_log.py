from datetime import datetime, timezone
import numpy as np
import pandas as pd
import puckpandas as pp
from sqlalchemy import text


class SeasonsImportLog:
    def __init__(self, team_id, season_id, games_found=0):
        self.team_id = team_id
        self.season_id = season_id
        self.games_found = games_found

    def insert_db(self):
        engine = pp.dba_import_login()
        sql = "insert into puckpandas_import.team_seasons_import_log (teamId, seasonId, lastDateUpdated, gamesFound) " \
              "values (:teamId, :seasonId, :lastDateUpdated, :gamesFound)"
        params = {'teamId': self.team_id, 'seasonId': self.season_id,
                  'lastDateUpdated': np.datetime64(datetime.now(timezone.utc).replace(tzinfo=None)).astype(str),
                  'gamesFound': self.games_found}
        with engine.connect() as conn:
            conn.execute(text(sql), parameters=params)

        return True

    def last_update(self):
        last_update = ''

        engine = pp.dba_import_login()
        prefix_sql = "select teamId, seasonId, max(lastDateUpdated) as lastDateUpdated from " \
                     "puckpandas_import.team_seasons_import_log where teamId = "
        mid_sql = " and seasonId = '"
        suffix_sql = "' group by teamId, seasonId"
        update_log_sql = "{}{}{}{}{}".format(prefix_sql, self.team_id, mid_sql, self.season_id, suffix_sql)
        update_df = pd.read_sql_query(update_log_sql, engine)
        engine.dispose()

        if update_df.size != 0:
            last_update = update_df['lastDateUpdated'].values[0]

        return last_update

    @staticmethod
    def seasons_without_games():
        engine = pp.dba_import_login()
        sql = "select a.seasonId, count(b.gameId) as gameCount from puckpandas_import.team_seasons_import as a left " \
              "join puckpandas_import.games_import as b on a.seasonId = b.seasonId group by a.seasonId having " \
              "gameCount = 0"
        seasons = pd.read_sql_query(sql, engine)
        engine.dispose()

        return seasons

    @staticmethod
    def seasons_without_rosters():
        engine = pp.dba_import_login()
        sql = "select a.seasonId, count(b.playerId) as playerCount from puckpandas_import.team_seasons_import as a " \
              "left join rosters_import as b on a.seasonId = b.seasonId group by a.seasonId having playerCount = 0"
        seasons = pd.read_sql_query(sql, engine)
        engine.dispose()

        return seasons
