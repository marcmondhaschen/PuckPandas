import pandas as pd
from .mysql_db import db_import_login


class PlayerImportLog:
    update_details = pd.Series(index=['playerId', 'lastDateUpdated', 'playerFound', 'careerTotalsFound',
                                      'seasonTotalsFound', 'awardsFound'])

    def __init__(self, player_id="", last_date_updated="", player_found=0, career_totals_found=0,
                 season_totals_found=0, awards_found=0):
        self.update_details['playerId'] = player_id
        self.update_details['lastDateUpdated'] = last_date_updated
        self.update_details['playerFound'] = player_found
        self.update_details['careerTotalsFound'] = career_totals_found
        self.update_details['seasonTotalsFound'] = season_totals_found
        self.update_details['awardsFound'] = awards_found

    @staticmethod
    def updateDB(self):
        if (len(self.update_details) > 0) and ('gameId' in self.update_details):
            cursor, db = db_import_login()

            sql = "insert into player_import_log (playerId, lastDateUpdated, playerFound, careerTotalsFound, " \
                  "seasonTotalsFound, awardsFound) values (%s, %s, %s, %s, %s, %s)"
            val = (self.update_details['playerId'], self.update_details['lastDateUpdated'],
                   self.update_details['playerFound'], self.update_details['careerTotalsFound'],
                   self.update_details['seasonTotalsFoundFound'], self.update_details['awardsFound'])
            cursor.execute(sql, val)

            db.commit()
            cursor.close()
            db.close()

        return True

    @staticmethod
    def queryDB(player_id='', player_found=1):
        cursor, db = db_import_login()

        prefix_sql = "select playerId, max(lastDateUpdated) as lastDateUpdated, " \
                     "playerFound from games_import_log where gameId = '"
        suffix_sql = "' and playerFound = "
        suffix2_sql = " group by playerId, updateFound"
        update_log_sql = "{}{}{}{}{}".format(prefix_sql, player_id, suffix_sql, player_found, suffix2_sql)
        update_df = pd.read_sql(update_log_sql, db)
        last_update_date = update_df.iloc[0]["lastDateUpdated"]

        db.commit()
        cursor.close()
        db.close()

        return last_update_date
