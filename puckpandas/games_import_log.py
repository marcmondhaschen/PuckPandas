from datetime import datetime, timezone
import numpy as np
import pandas as pd
import puckpandas
from sqlalchemy import text


class GamesImportLog:
    def __init__(self, game_id = '', game_found='', game_center_found='', tv_broadcasts_found='',
                 plays_found='', roster_spots_found='', team_game_stats_found='', season_series_found='',
                 referees_found='', linesmen_found='', scratches_found='', shifts_found=''):
        self.update_details = (
            pd.Series(dtype=str, index=['gameId', 'lastDateUpdated', 'gameFound', 'gameCenterFound',
                                        'tvBroadcastsFound', 'playsFound', 'rosterSpotsFound', 'teamGameStatsFound',
                                        'seasonSeriesFound', 'refereesFound', 'linesmenFound', 'scratchesFound',
                                        'shiftsFound']))
        self.update_details['gameId'] = game_id
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

    def insert_db(self):
        if self.update_details['gameId'] != '':
            if self.query_db(self.update_details['gameId']) != '':
                self.update_db()

                return True

            if self.update_details['gameId'] != '':
                engine = puckpandas.dba_import_login()
                sql = "insert into puckpandas_import.games_import_log (gameId, lastDateUpdated, gameFound, " \
                      "gameCenterFound, " \
                      "tvBroadcastsFound, playsFound, rosterSpotsFound, teamGameStatsFound, seasonSeriesFound, " \
                      "refereesFound, linesmenFound, scratchesFound, shiftsFound) values (:gameId, "\
                      ":lastDateUpdated, :gameFound, :gameCenterFound, :tvBroadcastsFound, :playsFound, "\
                      ":rosterSpotsFound, :teamGameStats, :seasonSeriesFound, :refereesFound, :linesmenFound, "\
                      ":scratchesFound, :shiftsFound)"
                params = {"gameId": self.update_details['gameId'],
                       "lastDateUpdated": np.datetime64(datetime.now(timezone.utc).replace(tzinfo=None)).astype(str),
                       "gameFound": self.update_details['gameFound'],
                       "gameCenterFound": self.update_details['gameCenterFound'],
                       "tvBroadcastsFound": self.update_details['tvBroadcastsFound'],
                       "playsFound": self.update_details['playsFound'],
                       "rosterSpotsFound": self.update_details['rosterSpotsFound'],
                       "teamGameStats": self.update_details['teamGameStatsFound'],
                       "seasonSeriesFound": self.update_details['seasonSeriesFound'],
                       "refereesFound": self.update_details['refereesFound'],
                       "linesmenFound": self.update_details['linesmenFound'],
                       "scratchesFound": self.update_details['scratchesFound'],
                       "shiftsFound": self.update_details['shiftsFound']}
                with engine.connect() as conn:
                    conn.execute(text(sql), parameters=params)

        return True

    def update_db(self):
        if self.update_details['gameId'] != '':
            if (len(self.update_details) > 0) and ('gameId' in self.update_details):
                engine = puckpandas.dba_import_login()

                set_string = "set lastDateUpdated = '" + \
                             np.datetime64(datetime.now(timezone.utc).replace(tzinfo=None)).astype(str) + "'"

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
                with engine.connect() as conn:
                    conn.execute(text(sql))

        return True

    @staticmethod
    def query_db(game_id):
        last_update = ''

        engine = puckpandas.dba_import_login()
        sql = "select gameId, max(lastDateUpdated) as lastDateUpdated, gameFound, gameCenterFound from " \
              "puckpandas_import.games_import_log where gameId = " + str(game_id) + " group by gameId, " \
              "gameFound, gameCenterFound"
        update_df = pd.read_sql_query(sql, engine)
        engine.dispose()

        if len(update_df.index) != 0:
            last_update = update_df['lastDateUpdated'].iloc[0]

        return last_update

    @staticmethod
    def games_not_queried():
        engine = puckpandas.dba_import_login()
        sql = "select gameId from puckpandas_import.games_import_log where (gameCenterFound is Null or " \
              "gameCenterFound = 0)"
        games_open_work_df = pd.read_sql_query(sql, engine)
        engine.dispose()

        return games_open_work_df

    @staticmethod
    def games_played_recently(start_date, stop_date):
        engine = puckpandas.dba_import_login()
        sql = "select gameId from puckpandas_import.games_import where gameDate between '" + str(start_date) + \
              "' and '" + str(stop_date) + "'"
        games_open_work_df = pd.read_sql_query(sql, engine)
        engine.dispose()

        return games_open_work_df

    @staticmethod
    def shifts_not_queried():
        engine = puckpandas.dba_import_login()
        sql = "select gameId from puckpandas_import.games_import_log where shiftsFound is Null"
        shifts_open_work_df = pd.read_sql_query(sql, engine)
        engine.dispose()

        return shifts_open_work_df

    @staticmethod
    def shifts_played_recently(start_date, stop_date):
        engine = puckpandas.dba_import_login()
        sql = "select a.gameId from puckpandas_import.games_import_log as a join puckpandas_import.games_import as b " \
              "on a.gameId = b.gameId where a.shiftsFound = 0 and b.gameDate between '" + str(start_date) + "' and '" \
              + str(stop_date) + "'"
        shifts_open_work_df = pd.read_sql_query(sql, engine)
        engine.dispose()

        return shifts_open_work_df

    @staticmethod
    def games_between_dates(begin_date, end_date):
        engine = puckpandas.dba_import_login()
        sql = "select gameId from puckpandas_import.games_import where gameDate between '" + str(begin_date) + \
              "' and '" + str(end_date) + "'"
        games = pd.read_sql_query(sql, engine)
        engine.dispose()

        return games
