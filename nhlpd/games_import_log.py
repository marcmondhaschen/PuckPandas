from datetime import datetime
import pandas as pd
from .mysql_db import db_import_login


class GamesImportLog:
    update_details = pd.Series(index=['gameId', 'lastDateUpdated', 'gameFound', 'tvBroadcastsFound', 'playsFound',
                                      'rosterSpotsFound', 'summaryFound', 'shiftsFound'])

    def __init__(self, game_id, last_date_updated, game_found='', tv_broadcasts_found='', plays_found='',
                 roster_spots_found='', summary_found='', shifts_found=''):
        self.update_details['gameId'] = game_id
        self.update_details['lastDateUpdated'] = last_date_updated
        self.update_details['gameFound'] = game_found
        self.update_details['tvBroadcastsFound'] = tv_broadcasts_found
        self.update_details['playsFound'] = plays_found
        self.update_details['rosterSpotsFound'] = roster_spots_found
        self.update_details['summaryFound'] = summary_found
        self.update_details['shiftsFound'] = shifts_found

    @staticmethod
    def insertDB(self):
        cursor, db = db_import_login()

        if (len(self.update_details) > 0) and ('gameId' in self.update_details):
            sql = "insert into games_import_log (gameId, lastDateUpdated, gameFound, tvBroadcastsFound, playsFound, " \
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
    def updateDB(self):
        if (len(self.update_details) > 0) and ('gameId' in self.update_details):
            cursor, db = db_import_login()

            set_string = "set lastDateUpdated = '" + datetime.today().strftime('%Y-%m-%d %H:%M:%S') + "'"

            if self.update_details['gameFound'] != '':
                set_string = set_string + ", gameFound = " + str(self.update_details['gameFound'])
            if self.update_details['tvBroadcastsFound'] != '':
                set_string = set_string + ", tvBroadcastsFound = " + str(self.update_details['tvBroadcastsFound'])
            if self.update_details['playsFound'] != '':
                set_string = set_string + ", playsFound = " + str(self.update_details['playsFound'])
            if self.update_details['rosterSpotsFound'] != '':
                set_string = set_string + ", rosterSpotsFound = " + str(self.update_details['rosterSpotsFound'])
            if self.update_details['summaryFound'] != '':
                set_string = set_string + ", summaryFound = " + str(self.update_details['summaryFound'])
            if self.update_details['shiftsFound'] != '':
                set_string = set_string + ", shiftsFound = " + str(self.update_details['shiftsFound'])

            sql_prefix = "update games_import_log "
            sql_mid = " where gameId = '"
            sql_suffix = "'"
            sql = "{}{}{}{}{}".format(sql_prefix, set_string, sql_mid, self.update_details['gameId'], sql_suffix)
            cursor.execute(sql)

            db.commit()
            cursor.close()
            db.close()

        return True

    @staticmethod
    def queryDB(game_id=''):
        cursor, db = db_import_login()

        prefix_sql = "select gameId, max(lastDateUpdated) as lastDateUpdated, " \
                     "gameFound from games_import_log where gameId = '"
        suffix_sql = "' group by gameId, updateFound"
        update_log_sql = "{}{}{}".format(prefix_sql, game_id, suffix_sql)
        update_df = pd.read_sql(update_log_sql, db)

        last_update = update_df.iloc[0]
        last_update = last_update.squeeze(axis=0)

        db.commit()
        cursor.close()
        db.close()

        return last_update
