from datetime import datetime, timezone
import pandas as pd
import nhlpd


class PlayerImportLog:
    def __init__(self, player_id='', last_date_updated='', player_found='', career_totals_found='',
                 season_totals_found='', awards_found=''):
        self.update_details = pd.Series(index=['playerId', 'lastDateUpdated', 'playerFound', 'careerTotalsFound',
                                      'seasonTotalsFound', 'awardsFound'])
        self.update_details['playerId'] = player_id
        self.update_details['lastDateUpdated'] = last_date_updated
        self.update_details['playerFound'] = player_found
        self.update_details['careerTotalsFound'] = career_totals_found
        self.update_details['seasonTotalsFound'] = season_totals_found
        self.update_details['awardsFound'] = awards_found

    def insert_db(self):
        if self.update_details['playerId'] != '':
            if self.query_db(self.update_details['playerId']) != '':
                self.update_db()

                return True

            cursor, db = nhlpd.db_import_login()

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

    def update_db(self):
        if (len(self.update_details) > 0) and ('playerId' in self.update_details):
            cursor, db = nhlpd.db_import_login()

            set_string = "set lastDateUpdated = '" + \
                         datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S') + "'"

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
    def query_db(player_id):
        last_update = ''

        cursor, db = nhlpd.db_import_login()
        sql = "select playerId, max(lastDateUpdated) as lastDateUpdated from player_import_log where playerId = " \
              + str(player_id) + " group by playerId"
        update_df = pd.read_sql(sql, db)
        db.commit()
        cursor.close()
        db.close()

        if len(update_df.index) != 0:
            last_update = update_df['lastDateUpdated'].iloc[0]

        return last_update

    @staticmethod
    def insert_untracked_players():
        cursor, db = nhlpd.db_import_login()
        untracked_players_sql = "select distinct a.playerId as playerId from roster_spots_import as a left join " \
                                "player_import_log as b on a.playerId = b.playerId where b.playerId is Null"
        untracked_players_df = pd.read_sql(untracked_players_sql, db)

        if untracked_players_df.size > 0:
            for index, row in untracked_players_df.iterrows():
                sql = "insert into player_import_log (playerId) values (%s)"
                val = (str(row['playerId']))
                cursor.execute(sql, (val,))

        db.commit()
        cursor.close()
        db.close()

        return True

    @staticmethod
    def players_not_queried():
        cursor, db = nhlpd.db_import_login()
        sql = "select playerId from player_import_log where playerFound is NULL"
        player_open_work_df = pd.read_sql(sql, db)
        db.commit()
        cursor.close()
        db.close()

        return player_open_work_df

    @staticmethod
    def players_played_recently(start_date, end_date):
        cursor, db = nhlpd.db_import_login()
        sql = ("select distinct b.playerId as playerId from roster_spots_import as b join (select gameId from "
               "games_import where gameDate between '" + str(start_date) + "' and '" + str(end_date) +
               "') as a on a.gameId = b.gameId")
        player_open_work_df = pd.read_sql(sql, db)
        db.commit()
        cursor.close()
        db.close()

        return player_open_work_df