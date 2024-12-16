from datetime import datetime, timezone
import pandas as pd
from .mysql_db import db_import_login


class SeasonImportLog:
    def __init__(self, team_id, season_id, games_found=0):
        self.team_id = team_id
        self.season_id = season_id
        self.current_time = datetime.now(timezone.utc)
        self.games_found = games_found

    def insertDB(self):
        cursor, db = db_import_login()

        sql = "insert into team_seasons_import_log (teamId, seasonId, lastDateUpdated, gamesFound) " \
              "values (%s, %s, %s, %s)"
        val = (self.team_id, self.season_id, self.current_time, self.games_found)
        cursor.execute(sql, val)

        db.commit()
        cursor.close()
        db.close()

        return True

    def lastUpdate(self):
        last_update = ''

        cursor, db = db_import_login()
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
