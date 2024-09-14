from datetime import datetime
import pandas as pd
from .mysql_db import db_import_login


class GamesImportLog:
    update_details = pd.Series(index=['gameId', 'lastDateUpdated', 'gameFound', 'gameCenterFound', 'tvBroadcastsFound',
                                      'playsFound', 'rosterSpotsFound', 'teamGameStatsFound', 'seasonSeriesFound',
                                      'linescoreByPeriodFound', 'refereesFound', 'linesmenFound', 'scratchesFound',
                                      'shiftsFound'])

    open_work_df = pd.DataFrame(columns=['gameId', 'lastDateUpdated'])

    def __init__(self, game_id='', last_date_updated='', game_found='', tv_broadcasts_found='', plays_found='',
                 roster_spots_found='', team_game_stats_found='', season_series_found='',
                 linescore_by_period_found='', referees_found='', linesmen_found='', scratches_found='',
                 shifts_found=''):
        self.update_details['gameId'] = game_id
        self.update_details['lastDateUpdated'] = last_date_updated
        self.update_details['gameFound'] = game_found
        self.update_details['tvBroadcastsFound'] = tv_broadcasts_found
        self.update_details['playsFound'] = plays_found
        self.update_details['rosterSpotsFound'] = roster_spots_found
        self.update_details['teamGameStatsFound'] = team_game_stats_found
        self.update_details['seasonSeriesFound'] = season_series_found
        self.update_details['linescoreByPeriodFound'] = linescore_by_period_found
        self.update_details['refereesFound'] = referees_found
        self.update_details['linesmenFound'] = linesmen_found
        self.update_details['scratchesFound'] = scratches_found
        self.update_details['shiftsFound'] = shifts_found

    @staticmethod
    def insertDB(self):
        if self.queryDB(self.update_details['gameId']) != '':
            self.updateDB(self)

            return True

        cursor, db = db_import_login()

        if self.update_details['gameId'] != '':
            sql = "insert into games_import_log (gameId, lastDateUpdated, gameFound, gameCenterFound, " \
                  "tvBroadcastsFound, playsFound, rosterSpotsFound, teamGameStatsFound, seasonSeriesFound, " \
                  "linescoreByPeriodFound, refereesFound, linesmenFound, scratchesFound, shiftsFound) " \
                  "values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            val = (self.update_details['gameId'], self.update_details['lastDateUpdated'],
                   self.update_details['gameFound'], self.update_details['gameCenterFound'],
                   self.update_details['tvBroadcastsFound'], self.update_details['playsFound'],
                   self.update_details['rosterSpotsFound'], self.update_details['teamGameStatsFound'],
                   self.update_details['seasonSeriesFound'], self.update_details['linescoreByPeriodFound'],
                   self.update_details['refereesFound'], self.update_details['linesmenFound'],
                   self.update_details['scratchesFound'], self.update_details['shiftsFound'])
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
            if self.update_details['gameCenterFound'] != '':
                set_string = set_string + ", gameCenterFound = " + str(self.update_details['gameCenterFound'])
            if self.update_details['tvBroadcastsFound'] != '':
                set_string = set_string + ", tvBroadcastsFound = " + str(self.update_details['tvBroadcastsFound'])
            if self.update_details['playsFound'] != '':
                set_string = set_string + ", playsFound = " + str(self.update_details['playsFound'])
            if self.update_details['rosterSpotsFound'] != '':
                set_string = set_string + ", rosterSpotsFound = " + str(self.update_details['rosterSpotsFound'])
            if self.update_details['teamGameStatsFound'] != '':
                set_string = set_string + ", teamGameStatsFound = " + str(self.update_details['teamGameStatsFound'])
            if self.update_details['seasonSeriesFound'] != '':
                set_string = set_string + ", seasonSeriesFound = " + str(self.update_details['seasonSeriesFound'])
            if self.update_details['linescoreByPeriodFound'] != '':
                set_string = set_string + ", linescoreByPeriodFound = " + \
                             str(self.update_details['linescoreByPeriodFound'])
            if self.update_details['refereesFound'] != '':
                set_string = set_string + ", refereesFound = " + str(self.update_details['refereesFound'])
            if self.update_details['linesmenFound'] != '':
                set_string = set_string + ", linesmenFound = " + str(self.update_details['linesmenFound'])
            if self.update_details['scratchesFound'] != '':
                set_string = set_string + ",scratchesFound  = " + str(self.update_details['scratchesFound'])
            if self.update_details['shiftsFound'] != '':
                set_string = set_string + ", shiftsFound = " + str(self.update_details['shiftsFound'])

            sql_prefix = "update games_import_log "
            sql_mid = " where gameId = "
            sql = "{}{}{}{}".format(sql_prefix, set_string, sql_mid, self.update_details['gameId'])
            cursor.execute(sql)

            db.commit()
            cursor.close()
            db.close()

        return True

    @staticmethod
    def queryDB(game_id):
        last_update = ''

        cursor, db = db_import_login()

        prefix_sql = "select gameId, max(lastDateUpdated) as lastDateUpdated from games_import_log where gameId = "
        suffix_sql = " group by gameId"
        update_log_sql = "{}{}{}".format(prefix_sql, game_id, suffix_sql)
        update_df = pd.read_sql(update_log_sql, db)

        db.commit()
        cursor.close()
        db.close()

        if len(update_df.index) != 0:
            last_update = update_df['lastDateUpdated'].iloc[0]

        return last_update

    def updateOpenWork(self):
        cursor, db = db_import_login()
        sql = "select gameId, lastDateUpdated from games_import_log where (gameCenterFound is NULL or " \
              "gameCenterFound = 0)"
        self.open_work_df = pd.read_sql(sql, db)

        db.commit()
        cursor.close()
        db.close()

        return True
