import pandas as pd
from .mysql_db import db_import_login


class GamesImportLog:
    update_details = pd.Series(index=['gameId', 'lastDateUpdated', 'gameFound', 'tvBroadcastsFound', 'playsFound',
                                      'rosterSpotsFound', 'summaryFound', 'shiftsFound'])

    def __init__(self, game_id="", last_date_updated="", game_found=0, tv_broadcasts_found=0, plays_found=0,
                 roster_spots_found=0, summary_found=0, shifts_found=0):
        self.update_details['gameId'] = game_id
        self.update_details['lastDateUpdated'] = last_date_updated
        self.update_details['gameFound'] = game_found
        self.update_details['tvBroadcastsFound'] = tv_broadcasts_found
        self.update_details['playsFound'] = plays_found
        self.update_details['rosterSpotsFound'] = roster_spots_found
        self.update_details['summaryFound'] = summary_found
        self.update_details['shiftsFound'] = shifts_found

    @staticmethod
    def updateDB(self):
        if (len(self.update_details) > 0) and ('gameId' in self.update_details):
            cursor, db = db_import_login()

            sql = "insert into games_update_log (gameId, lastDateUpdated, gameFound, tvBroadcastsFound, playsFound, " \
                  "rosterSpotsFound, summaryFound, shiftsFound) values (%s, %s, %s, %s, %s, %s, %s, %s)"
            val = (self.update_details['gameId'], self.update_details['lastDateUpdated'],
                   self.update_details['gameFound'], self.update_details['tvBroadcastsFound'],
                   self.update_details['playsFound'], self.update_details['rosterSpotsFound'],
                   self.update_details['summaryFound'], self.update_details['shiftsFound'])
            cursor.execute(sql, val)

            db.commit()
            cursor.close()
            db.close()

        return True

    @staticmethod
    def queryDB(game_id='', game_found=1):
        cursor, db = db_import_login()

        prefix_sql = "select gameId, max(lastDateUpdated) as lastDateUpdated, " \
                     "gameFound from games_import_log where gameId = '"
        suffix_sql = "' and gameFound = "
        suffix2_sql = " group by gameId, updateFound"
        update_log_sql = "{}{}{}{}{}".format(prefix_sql, game_id, suffix_sql, game_found, suffix2_sql)
        update_df = pd.read_sql(update_log_sql, db)
        last_update_date = update_df.iloc[0]["lastDateUpdated"]

        db.commit()
        cursor.close()
        db.close()

        return last_update_date
