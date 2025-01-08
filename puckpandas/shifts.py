import pandas as pd
import puckpandas
from sqlalchemy import text

""" shift details first appear in the NHL's API set in the 20102011 season """
class ShiftsImport:
    def __init__(self, game_id):
        self.game_id = game_id
        self.table_columns = ['id', 'detailCode', 'duration', 'endTime', 'eventDescription', 'eventDetails',
                              'eventNumber', 'firstName', 'gameId', 'hexValue', 'lastName', 'period', 'playerId',
                              'shiftNumber', 'startTime', 'teamAbbrev', 'teamId', 'teamName', 'typeCode']
        self.shifts_df = pd.DataFrame()
        self.query_db()

    def update_db(self):
        shifts_found = 0
        if self.shifts_df.size > 0:
            shifts_found = 1

            engine = puckpandas.dba_import_login()
            sql = "insert into puckpandas_import.shifts_import (id, detailCode, duration, endTime, eventDescription, " \
                  "eventDetails, " \
                  "eventNumber, firstName, gameId, hexValue, lastName, period, playerId, shiftNumber, startTime, " \
                  "teamAbbrev, teamId, teamName, typeCode) values (:id, :detailCode, :duration, :endTime, " \
                  ":eventDescription, :eventDetails, :eventNumber, :firstName, :gameId, :hexValue, :lastName, " \
                  ":period, :playerId, :shiftNumber, :startTime, :teamAbbrev, :teamId, :teamName, :typeCode)"
            shifts_df = self.shifts_df.fillna('')
            params = shifts_df.to_dict('records')
            with engine.connect() as conn:
                conn.execute(text(sql), parameters=params)

        log = puckpandas.GamesImportLog(game_id=self.game_id, shifts_found=shifts_found)
        log.update_db()

        return True

    def clear_db(self):
        engine = puckpandas.dba_import_login()
        sql = "delete from puckpandas_import.shifts_import where gameId =" + str(self.game_id)
        with engine.connect() as conn:
            conn.execute(text(sql))

        return True

    def query_db(self):
        engine = puckpandas.dba_import_login()
        sql = "select id, detailCode, duration, endTime, eventDescription, eventDetails, eventNumber, firstName, " \
              "gameId, hexValue, lastName, period, playerId, shiftNumber, startTime, teamAbbrev, teamId, teamName, " \
              "typeCode from puckpandas_import.shifts_import where gameId = " + str(self.game_id)
        shifts_df = pd.read_sql_query(sql, engine)
        engine.dispose()

        if shifts_df.size > 0:
            shifts_df.fillna(0, inplace=True)
            self.shifts_df = shifts_df

        self.shifts_df.reindex(columns=self.table_columns)

        return True

    def query_api(self):
        url_prefix = 'https://api.nhle.com/stats/rest/en/shiftcharts?cayenneExp=gameId='
        url_string = "{}{}".format(url_prefix, self.game_id)
        json_data = puckpandas.fetch_json_data(url_string)

        if len(json_data['data']) > 0:
            shifts_df = pd.json_normalize(json_data, record_path=['data'])
            shifts_df.reindex(columns=self.table_columns)
            self.shifts_df = shifts_df

        return True

    def query_api_update_db(self):
        self.query_api()
        self.clear_db()
        self.update_db()

        return True
