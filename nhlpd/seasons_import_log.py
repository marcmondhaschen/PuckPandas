from datetime import datetime, timezone
import numpy as np
import pandas as pd
import nhlpd


class SeasonsImportLog:
    def __init__(self, team_id, season_id, games_found=0):
        self.team_id = team_id
        self.season_id = season_id
        self.games_found = games_found

    def insert_db(self):
        cursor, db = nhlpd.db_import_login()

        sql = "insert into team_seasons_import_log (teamId, seasonId, lastDateUpdated, gamesFound) " \
              "values (%s, %s, %s, %s)"
        val = (self.team_id, self.season_id, np.datetime64(datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")),
               self.games_found)
        cursor.execute(sql, val)

        db.commit()
        cursor.close()
        db.close()

        return True

    def last_update(self):
        last_update = ''

        cursor, db = nhlpd.db_import_login()
        prefix_sql = "select teamId, seasonId, max(lastDateUpdated) as lastDateUpdated from " \
                     "team_seasons_import_log where teamId = "
        mid_sql = " and seasonId = '"
        suffix_sql = "' group by teamId, seasonId"
        update_log_sql = "{}{}{}{}{}".format(prefix_sql, self.team_id, mid_sql, self.season_id, suffix_sql)
        update_df = pd.read_sql(update_log_sql, db)
        db.commit()
        cursor.close()
        db.close()

        if update_df.size != 0:
            last_update = update_df['lastDateUpdated'].values[0]

        return last_update

    @staticmethod
    def seasons_without_games():
        cursor, db = nhlpd.db_import_login()
        sql = "select a.seasonId, count(b.gameId) as gameCount from team_seasons_import as a left join games_import " \
              "as b on a.seasonId = b.seasonId group by a.seasonId having gameCount = 0"
        seasons = pd.read_sql(sql, db)
        db.commit()
        cursor.close()
        db.close()

        return seasons

    @staticmethod
    def seasons_without_rosters():
        cursor, db = nhlpd.db_import_login()
        sql = "select a.seasonId, count(b.playerId) as playerCount from team_seasons_import as a left join " \
              "rosters_import as b on a.seasonId = b.seasonId group by a.seasonId having playerCount = 0"
        seasons = pd.read_sql(sql, db)
        db.commit()
        cursor.close()
        db.close()

        return seasons

