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
        val = (self.team_id, self.season_id, np.datetime_as_string(np.datetime64(datetime.now(timezone.utc))),
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
