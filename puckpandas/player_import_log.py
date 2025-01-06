from datetime import datetime, timezone
import numpy as np
import pandas as pd
import puckpandas
from sqlalchemy import text

class PlayerImportLog:
    def __init__(self, player_id='', player_found='', career_totals_found='',
                 season_totals_found='', awards_found=''):
        self.update_details = pd.Series(index=['playerId', 'lastDateUpdated', 'playerFound', 'careerTotalsFound',
                                      'seasonTotalsFound', 'awardsFound']).astype(object)
        self.update_details['playerId'] = player_id
        self.update_details['playerFound'] = player_found
        self.update_details['careerTotalsFound'] = career_totals_found
        self.update_details['seasonTotalsFound'] = season_totals_found
        self.update_details['awardsFound'] = awards_found

    def insert_db(self):
        if self.update_details['playerId'] != '':
            if self.query_db(self.update_details['playerId']) != '':
                self.update_db()
                return True

            if self.update_details['playerId'] != '':
                engine = puckpandas.dba_import_login()
                sql = "insert into player_import_log (playerId, lastDateUpdated, playerFound, careerTotalsFound, " \
                      "seasonTotalsFound, awardsFound) values (:playerId, :lastDateUpdated, :playerFound, " \
                      ":careerTotalsFound, :seasonTotalsFound, :awardsFound)"
                params = {'playerId': self.update_details['playerId'],
                          'lastDateUpdated': np.datetime64(datetime.now(timezone.utc).replace(tzinfo=None)).astype(str),
                          'playerFound': self.update_details['playerFound'],
                          'careerTotalsFound': self.update_details['careerTotalsFound'],
                          'seasonTotalsFound': self.update_details['seasonTotalsFound'],
                          'awardsFound': self.update_details['awardsFound']}
                with engine.connect() as conn:
                    conn.execute(text(sql), parameters=params)

        return True

    def update_db(self):
        if (len(self.update_details) > 0) and ('playerId' in self.update_details):
            engine = puckpandas.dba_import_login()

            set_string = ("set lastDateUpdated = '" +
                          np.datetime64(datetime.now(timezone.utc).replace(tzinfo=None)).astype(str) + "'")

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
            with engine.connect() as conn:
                conn.execute(text(sql))

        return True

    @staticmethod
    def query_db(player_id):
        last_update = ''

        engine = puckpandas.dba_import_login()
        sql = "select playerId, max(lastDateUpdated) as lastDateUpdated from player_import_log where playerId = " \
              + str(player_id) + " group by playerId"
        update_df = pd.read_sql_query(sql, engine)
        engine.dispose()

        if len(update_df.index) != 0:
            last_update = update_df['lastDateUpdated'].iloc[0]

        return last_update

    @staticmethod
    def insert_untracked_players():
        engine = puckpandas.dba_import_login()
        untracked_players_sql = "select distinct a.playerId as playerId from roster_spots_import as a left join " \
                                "player_import_log as b on a.playerId = b.playerId where b.playerId is Null"
        untracked_players_df = pd.read_sql_query(untracked_players_sql, engine)
        engine.dispose()

        if untracked_players_df.size > 0:
            engine = puckpandas.dba_import_login()
            sql = "insert into player_import_log (playerId) values (:playerId)"
            params = untracked_players_df.to_dict('records')
            with engine.connect() as conn:
                conn.execute(text(sql), parameters=params)

        return True

    @staticmethod
    def players_not_queried():
        engine = puckpandas.dba_import_login()
        sql = "select playerId from player_import_log where playerFound is NULL"
        player_open_work_df = pd.read_sql_query(sql, engine)
        engine.dispose()

        return player_open_work_df

    @staticmethod
    def players_played_recently(start_date, end_date):
        engine = puckpandas.dba_import_login()
        sql = "select distinct b.playerId as playerId from roster_spots_import as b join (select gameId from " \
              "games_import where gameDate between '" + str(start_date) + "' and '" + str(end_date) + \
              "') as a on a.gameId = b.gameId"
        player_open_work_df = pd.read_sql_query(sql, engine)
        engine.dispose()

        return player_open_work_df