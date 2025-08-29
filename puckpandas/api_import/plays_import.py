import pandas as pd
import puckpandas as pp
from sqlalchemy import text


class PlaysImport:
    def __init__(self, game_id):
        self.game_id = game_id
        self.json = {}
        self.table_columns = ['gameId', 'eventId', 'periodDescriptor.number', 'periodDescriptor.periodType',
                              'periodDescriptor.maxRegulationPeriods', 'timeInPeriod', 'timeRemaining', 'situationCode',
                              'homeTeamDefendingSide', 'typeCode', 'typeDescKey', 'sortOrder',
                              'details.eventOwnerTeamId', 'details.losingPlayerId', 'details.winningPlayerId',
                              'details.xCoord', 'details.yCoord', 'details.zoneCode', 'details.reason',
                              'details.hittingPlayerId', 'details.hitteePlayerId', 'details.shotType',
                              'details.shootingPlayerId', 'details.goalieInNetId', 'details.awaySOG', 'details.homeSOG',
                              'details.playerId', 'details.blockingPlayerId', 'details.secondaryReason',
                              'details.typeCode', 'details.descKey', 'details.duration',
                              'details.committedByPlayerId', 'details.drawnByPlayerId',
                              'details.scoringPlayerId', 'details.scoringPlayerTotal', 'details.assist1PlayerId',
                              'details.assist1PlayerTotal', 'details.assist2PlayerId', 'details.assist2PlayerTotal',
                              'details.awayScore', 'details.homeScore']
        self.plays_df = pd.DataFrame()
        self.query_db()
        self.plays_df = self.plays_df.reindex(columns=self.table_columns)

    def update_db(self):
        plays_found = 0
        if self.plays_df.size > 0:
            plays_found = 1

            engine = pp.dba_import_login()
            sql = "insert into puckpandas_import.plays_import (gameId, eventId, `periodDescriptor.number`, " \
                  "`periodDescriptor.periodType`, `periodDescriptor.maxRegulationPeriods`, timeInPeriod, " \
                  "timeRemaining, situationCode, homeTeamDefendingSide, typeCode, typeDescKey, sortOrder, " \
                  "`details.eventOwnerTeamId`, `details.losingPlayerId`, `details.winningPlayerId`, `details.xCoord`, "\
                  "`details.yCoord`, `details.zoneCode`, `details.reason`, `details.hittingPlayerId`, " \
                  "`details.hitteePlayerId`, `details.shotType`, `details.shootingPlayerId`, `details.goalieInNetId`, "\
                  "`details.awaySOG`, `details.homeSOG`, `details.playerId`, `details.blockingPlayerId`, "\
                  "`details.secondaryReason`, `details.TypeCode`, `details.DescKey`, " \
                  "`details.Duration`, `details.CommittedByPlayerId`, `details.DrawnByPlayerId`, " \
                  "`details.scoringPlayerId`, `details.scoringPlayerTotal`, `details.assist1PlayerId`, " \
                  "`details.assist1PlayerTotal`, `details.assist2PlayerId`, `details.assist2PlayerTotal`, " \
                  "`details.awayScore`, `details.homeScore`) values (:gameId, :eventId, :periodDescriptornumber, " \
                  ":periodDescriptorperiodType, :periodDescriptormaxRegulationPeriods, :timeInPeriod, " \
                  ":timeRemaining, :situationCode, :homeTeamDefendingSide, :typeCode, :typeDescKey, :sortOrder, " \
                  ":detailseventOwnerTeamId, :detailslosingPlayerId, :detailswinningPlayerId, :detailsxCoord, " \
                  ":detailsyCoord, :detailszoneCode, :detailsreason, :detailshittingPlayerId, " \
                  ":detailshitteePlayerId, :detailsshotType, :detailsshootingPlayerId, :detailsgoalieInNetId, " \
                  ":detailsawaySOG, :detailshomeSOG, :detailsplayerId, :detailsblockingPlayerId, " \
                  ":detailssecondaryReason, :detailstypeCode, :detailsdescKey, :detailsduration, " \
                  ":detailscommittedByPlayerId, :detailsdrawnByPlayerId, :detailsscoringPlayerId, " \
                  ":detailsscoringPlayerTotal, :detailsassist1PlayerId, :detailsassist1PlayerTotal, " \
                  ":detailsassist2PlayerId, :detailsassist2PlayerTotal, :detailsawayScore, :detailshomeScore)"
            plays_df = self.plays_df
            plays_df.columns = plays_df.columns.str.replace('.', '')
            params = plays_df.to_dict('records')

            with engine.connect() as conn:
                conn.execute(text(sql), parameters=params)

        log = pp.GamesImportLog(game_id=self.game_id, plays_found=plays_found)
        log.insert_db()

        return True

    def clear_db(self):
        engine = pp.dba_import_login()
        sql = "delete from puckpandas_import.plays_import where gameId = " + str(self.game_id)
        with engine.connect() as conn:
            conn.execute(text(sql))

        return True

    def query_db(self):
        engine = pp.dba_import_login()
        sql = "select gameId, eventId, `periodDescriptor.number`, `periodDescriptor.periodType`, " \
              "`periodDescriptor.maxRegulationPeriods`, timeInPeriod, timeRemaining, situationCode, " \
              "homeTeamDefendingSide, typeCode, typeDescKey, sortOrder, `details.eventOwnerTeamId`, " \
              "`details.losingPlayerId`, `details.winningPlayerId`, `details.xCoord`, `details.yCoord`, " \
              "`details.zoneCode`, `details.reason`, `details.hittingPlayerId`, `details.hitteePlayerId`, " \
              "`details.shotType`, `details.shootingPlayerId`, `details.goalieInNetId`, `details.awaySOG`, " \
              "`details.homeSOG`, `details.playerId`, `details.blockingPlayerId`, `details.secondaryReason`, " \
              "`details.typeCode`, `details.descKey`, `details.duration`, " \
              "`details.committedByPlayerId`, `details.drawnByPlayerId`, `details.scoringPlayerId`, " \
              "`details.scoringPlayerTotal`, `details.assist1PlayerId`, `details.assist1PlayerTotal`, " \
              "`details.assist2PlayerId`, `details.assist2PlayerTotal`, `details.awayScore`, `details.homeScore` " \
              "from puckpandas_import.plays_import where gameId = " + str(self.game_id)
        plays_df = pd.read_sql_query(sql, engine)
        engine.dispose()

        if plays_df.size > 0:
            plays_df = plays_df.reindex(columns=self.table_columns)
            plays_df.infer_objects().fillna('', inplace=True)
            self.plays_df = plays_df

        return True

    def query_api(self):
        plays_df = pd.json_normalize(self.json)
        plays_df.insert(0, 'gameId', self.game_id)

        if plays_df.size > 0:
            plays_df = plays_df.reindex(columns=self.table_columns)
            plays_df.fillna(0, inplace=True)
            self.plays_df = plays_df

        return True

    def query_api_update_db(self):
        self.query_api()
        self.clear_db()
        self.update_db()

        return True
