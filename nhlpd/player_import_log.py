from datetime import datetime
import pandas as pd
from .mysql_db import db_import_login


class PlayerImportLog:
    update_details = pd.Series(index=['playerId', 'lastDateUpdated', 'playerFound', 'careerTotalsFound',
                                      'seasonTotalsFound', 'awardsFound'])

    player_bio_open_work_df = pd.DataFrame(columns=['playerId', 'lastDateUpdated'])

    def __init__(self, player_id='', last_date_updated='', player_found='', career_totals_found='',
                 season_totals_found='', awards_found=''):
        self.update_details['playerId'] = player_id
        self.update_details['lastDateUpdated'] = last_date_updated
        self.update_details['playerFound'] = player_found
        self.update_details['careerTotalsFound'] = career_totals_found
        self.update_details['seasonTotalsFound'] = season_totals_found
        self.update_details['awardsFound'] = awards_found

    def insertDB(self):
        if self.queryDB(self.update_details['playerId']) != '':
            self.updateDB()

            return True

        cursor, db = db_import_login()

        if self.update_details['playerId'] != '':
            sql = "insert into player_import_log (playerId, lastDateUpdated, playerFound, careerTotalsFound, " \
                  "seasonTotalsFound, awardsFound) values (%s, %s, %s, %s, %s, %s)"
            val = (self.update_details['playerId'], self.update_details['lastDateUpdated'],
                   self.update_details['playerFound'], self.update_details['careerTotalsFound'],
                   self.update_details['seasonTotalsFound'], self.update_details['awardsFound'])
            cursor.execute(sql, val)

        db.commit()
        cursor.close()
        db.close()

        return True

    def updateDB(self):
        if (len(self.update_details) > 0) and ('playerId' in self.update_details):
            cursor, db = db_import_login()

            set_string = "set lastDateUpdated = '" + datetime.today().strftime('%Y-%m-%d %H:%M:%S') + "'"

            if self.update_details['playerFound'] != '':
                set_string = set_string + ", playerFound = " + str(self.update_details['playerFound'])
            if self.update_details['careerTotalsFound'] != '':
                set_string = set_string + ", careerTotalsFound = " + str(self.update_details['careerTotalsFound'])
            if self.update_details['seasonTotalsFound'] != '':
                set_string = set_string + ", seasonTotalsFound = " + str(self.update_details['seasonTotalsFound'])
            if self.update_details['awardsFound'] != '':
                set_string = set_string + ", awardsFound = " + str(self.update_details['awardsFound'])

            sql_prefix = "update player_import_log "
            sql_mid = " where playerId = '"
            sql_suffix = "'"
            sql = "{}{}{}{}{}".format(sql_prefix, set_string, sql_mid, self.update_details['playerId'], sql_suffix)
            cursor.execute(sql)

            db.commit()
            cursor.close()
            db.close()

        return True

    @staticmethod
    def queryDB(player_id):
        last_update = ''

        cursor, db = db_import_login()

        prefix_sql = "select playerId, max(lastDateUpdated) as lastDateUpdated from games_import_log where playerId = "
        suffix_sql = " group by playerId"
        update_log_sql = "{}{}{}".format(prefix_sql, player_id, suffix_sql)
        update_df = pd.read_sql(update_log_sql, db)

        db.commit()
        cursor.close()
        db.close()

        if len(update_df.index) != 0:
            last_update = update_df['lastDateUpdated'].iloc[0]

        return last_update

    def playerOpenWork(self):
        cursor, db = db_import_login()
        sql = "select playerId, lastDateUpdated from player_import_log where (playerBioFound is NULL or " \
              "playerBioFound = 0)"
        self.player_bio_open_work_df = pd.read_sql(sql, db)

        db.commit()
        cursor.close()
        db.close()

        return True

# from players.py
#         check_date = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
#         check_log_df = pd.DataFrame(data=[[player_id, check_date, player_bio_check, career_check, season_check,
#                                            awards_check]],
#                                     columns=['playerId', 'logDate', 'playerBio', 'career', 'season', 'awards'])
#         check_log_df = check_log_df.fillna('')
#         update_player_log(check_log_df)
