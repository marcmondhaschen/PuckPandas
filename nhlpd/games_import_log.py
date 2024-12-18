from datetime import datetime, timezone
import pandas as pd
from .mysql_db import db_import_login


class GamesImportLog:
    update_details = pd.Series(index=['gameId', 'lastDateUpdated', 'gameFound', 'gameCenterFound', 'tvBroadcastsFound',
                                      'playsFound', 'rosterSpotsFound', 'teamGameStatsFound', 'seasonSeriesFound',
                                      'linescoreByPeriodFound', 'refereesFound', 'linesmenFound', 'scratchesFound',
                                      'shiftsFound'])
    game_center_open_work_df = pd.DataFrame(columns=['gameId', 'lastDateUpdated'])
    shifts_open_work_df = pd.DataFrame(columns=['gameId', 'lastDateUpdated'])

    def __init__(self, game_id, last_date_updated='', game_found='', game_center_found='', tv_broadcasts_found='',
                 plays_found='', roster_spots_found='', team_game_stats_found='', season_series_found='',
                 referees_found='', linesmen_found='', scratches_found='', shifts_found=''):
        self.update_details['gameId'] = game_id
        self.update_details['lastDateUpdated'] = last_date_updated
        self.update_details['gameFound'] = game_found
        self.update_details['gameCenterFound'] = game_center_found
        self.update_details['tvBroadcastsFound'] = tv_broadcasts_found
        self.update_details['playsFound'] = plays_found
        self.update_details['rosterSpotsFound'] = roster_spots_found
        self.update_details['teamGameStatsFound'] = team_game_stats_found
        self.update_details['seasonSeriesFound'] = season_series_found
        self.update_details['refereesFound'] = referees_found
        self.update_details['linesmenFound'] = linesmen_found
        self.update_details['scratchesFound'] = scratches_found
        self.update_details['shiftsFound'] = shifts_found

    def insertDB(self):
        if self.queryDB() != '':
            self.updateDB()

            return True

        if self.update_details['gameId'] != '':
            cursor, db = db_import_login()
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

    def updateDB(self):
        if (len(self.update_details) > 0) and ('gameId' in self.update_details):
            cursor, db = db_import_login()

            set_string = "set lastDateUpdated = '" + \
                         datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S') + "'"

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

    def queryDB(self):
        last_update = ''

        cursor, db = db_import_login()
        sql = "select gameId, max(lastDateUpdated), gameFound, gameCenterFound as lastDateUpdated from " \
              "games_import_log where gameId = " + str(self.update_details['gameId']) + " group by gameId, " \
              "gameFound, gameCenterFound"
        update_df = pd.read_sql(sql, db)
        db.commit()
        cursor.close()
        db.close()

        if len(update_df.index) != 0:
            last_update = update_df['lastDateUpdated'].iloc[0]

        return last_update
