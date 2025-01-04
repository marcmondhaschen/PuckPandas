import pandas as pd
import nhlpd
from sqlalchemy import text


class ScratchesImport:
    def __init__(self, game_id):
        self.game_id = game_id
        self.json = {}
        self.table_columns = ['gameId', 'playerId', 'firstName.default', 'lastName.default']
        self.scratches_df = pd.DataFrame()
        self.query_db()
        self.scratches_df = self.scratches_df.reindex(columns=self.table_columns)

    def update_db(self):
        scratches_found = 0
        if self.scratches_df.size > 0:
            scratches_found = 1

            engine = nhlpd.dba_import_login()
            sql = "insert into scratches_import (gameId, playerId, `firstName.default`, `lastName.default`) " \
                  "values (:gameId, :playerId, :firstNamedefault, :lastNamedefault)"
            scratches_df = self.scratches_df
            scratches_df.columns = scratches_df.columns.str.replace('.', '')
            params = scratches_df.to_dict('records')
            with engine.connect() as conn:
                conn.execute(text(sql), parameters=params)

        log = nhlpd.GamesImportLog(game_id=self.game_id, scratches_found=scratches_found)
        log.insert_db()

        return True

    def clear_db(self):
        engine = nhlpd.dba_import_login()
        sql = "delete from scratches_import where gameId = " + str(self.game_id)
        with engine.connect() as conn:
            conn.execute(text(sql))

        return True

    def query_db(self):
        engine = nhlpd.dba_import_login()
        sql = "select gameId, playerId, `firstName.default`, `lastName.default` from scratches_import where " \
              "gameId = " + str(self.game_id)
        scratches_df = pd.read_sql_query(sql, engine)
        engine.dispose()

        if scratches_df.size > 0:
            scratches_df = scratches_df.reindex(columns=self.table_columns)
            scratches_df.infer_objects().fillna('', inplace=True)
            self.scratches_df = scratches_df

        return True

    def query_nhl(self):
        scratches_df = pd.json_normalize(self.json)
        scratches_df.insert(0, 'gameId', self.game_id)
        scratches_df.rename(columns={"id": "playerId"}, inplace=True)

        if scratches_df.size > 0:
            scratches_df = scratches_df.reindex(columns=self.table_columns)
            scratches_df.infer_objects().fillna('', inplace=True)
            self.scratches_df = scratches_df

        return True

    def query_nhl_update_db(self):
        self.query_nhl()
        self.clear_db()
        self.update_db()

        return True


class LinesmenImport:
    def __init__(self, game_id):
        self.game_id = game_id
        self.json = {}
        self.table_columns = ['gameId', 'default']
        self.linesmen_df = pd.DataFrame()
        self.query_db()
        self.linesmen_df = self.linesmen_df.reindex(columns=self.table_columns)

    def update_db(self):
        linesmen_found = 0
        if self.linesmen_df.size > 0:
            linesmen_found = 1

            engine = nhlpd.dba_import_login()
            sql = "insert into linesmen_import (gameId, `default`) values (:gameId, :default)"
            params = self.linesmen_df.to_dict('records')
            with engine.connect() as conn:
                conn.execute(text(sql), parameters=params)

        log = nhlpd.GamesImportLog(game_id=self.game_id,
                                   linesmen_found=linesmen_found)
        log.insert_db()

        return True

    def clear_db(self):
        engine = nhlpd.dba_import_login()
        sql = "delete from linesmen_import where gameId = " + str(self.game_id)
        with engine.connect() as conn:
            conn.execute(text(sql))

        return True

    def query_db(self):
        engine = nhlpd.dba_import_login()
        sql = "select gameId, `default` from linesmen_import where gameId = " + str(self.game_id)
        linesmen_df = pd.read_sql_query(sql, engine)
        engine.dispose()

        if linesmen_df.size > 0:
            linesmen_df = linesmen_df.reindex(columns=self.table_columns)
            linesmen_df.infer_objects().fillna('', inplace=True)
            self.linesmen_df = linesmen_df

        return True

    def query_nhl(self):
        linesmen_df = pd.json_normalize(self.json)
        linesmen_df.insert(0, 'gameId', self.game_id)

        if linesmen_df.size > 0:
            linesmen_df = linesmen_df.reindex(columns=self.table_columns)
            linesmen_df.infer_objects().fillna('', inplace=True)
            self.linesmen_df = linesmen_df

        return True

    def query_nhl_update_db(self):
        self.query_nhl()
        self.clear_db()
        self.update_db()

        return True


class RefereesImport:
    def __init__(self, game_id):
        self.game_id = game_id
        self.json = {}
        self.table_columns = ['gameId', 'default']
        self.referees_df = pd.DataFrame()
        self.query_db()
        self.referees_df = self.referees_df.reindex(columns=self.table_columns)

    def update_db(self):
        referees_found = 0
        if self.referees_df.size > 0:
            referees_found = 1

            engine = nhlpd.dba_import_login()
            sql = "insert into referees_import (gameId, `default`) values (:gameId, :default)"
            params = self.referees_df.to_dict('records')
            with engine.connect() as conn:
                conn.execute(text(sql), parameters=params)

        log = nhlpd.GamesImportLog(game_id=self.game_id, referees_found=referees_found)
        log.insert_db()

        return True

    def clear_db(self):
        engine = nhlpd.dba_import_login()
        sql = "delete from referees_import where gameId = " + str(self.game_id)
        with engine.connect() as conn:
            conn.execute(text(sql))

        return True

    def query_db(self):
        engine = nhlpd.dba_import_login()
        sql = "select gameId, `default` from referees_import where gameId = " + str(self.game_id)
        referees_df = pd.read_sql_query(sql, engine)
        engine.dispose()

        if referees_df.size > 0:
            referees_df = referees_df.reindex(columns=self.table_columns)
            referees_df.infer_objects().fillna('', inplace=True)
            self.referees_df = referees_df

        return True

    def query_nhl(self):
        referees_df = pd.json_normalize(self.json)
        referees_df.insert(0, 'gameId', self.game_id)

        if referees_df.size > 0:
            referees_df = referees_df.reindex(columns=self.table_columns)
            referees_df.infer_objects().fillna('', inplace=True)
            self.referees_df = referees_df

        return True

    def query_nhl_update_db(self):
        self.query_nhl()
        self.clear_db()
        self.update_db()

        return True


class SeasonSeriesImport:
    def __init__(self, game_id):
        self.game_id = game_id
        self.json = {}
        self.table_columns = ['gameId', 'seriesNumber', 'refGameId']
        self.season_series_df = pd.DataFrame()
        self.query_db()
        self.season_series_df = self.season_series_df.reindex(columns=self.table_columns)

    def update_db(self):
        season_series_found = 0
        if self.season_series_df.size > 0:
            season_series_found = 1

            engine = nhlpd.dba_import_login()
            sql = "insert into season_series_import (gameId, seriesNumber, refGameId) values (:gameId, " \
                  ":seriesNumber, :refGameId)"
            params = self.season_series_df.to_dict('records')
            with engine.connect() as conn:
                conn.execute(text(sql), parameters=params)

        log = nhlpd.GamesImportLog(game_id=self.game_id, season_series_found=season_series_found)
        log.insert_db()

        return True

    def clear_db(self):
        engine = nhlpd.dba_import_login()
        sql = "delete from season_series_import where gameId = " + str(self.game_id)
        with engine.connect() as conn:
            conn.execute(text(sql))

        return True

    def query_db(self):
        engine = nhlpd.dba_import_login()
        sql = "select gameId, seriesNumber, refGameId from season_series_import where gameId = " + str(self.game_id)
        season_series_df = pd.read_sql_query(sql, engine)
        engine.dispose()

        if season_series_df.size > 0:
            season_series_df = season_series_df.reindex(columns=self.table_columns)
            season_series_df.infer_objects().fillna('', inplace=True)
            self.season_series_df = season_series_df

        return True

    def query_nhl(self):
        season_series_df = pd.json_normalize(self.json)
        # noinspection PyTypeChecker
        season_series_df.insert(0, 'seriesNumber', range(len(season_series_df)))
        season_series_df.insert(0, 'gameId', self.game_id)
        season_series_df.rename(columns={"id": "refGameId"}, inplace=True)

        if season_series_df.size > 0:
            season_series_df = season_series_df.reindex(columns=self.table_columns)
            season_series_df.infer_objects().fillna('', inplace=True)
            self.season_series_df = season_series_df

        return True

    def query_nhl_update_db(self):
        self.query_nhl()
        self.clear_db()
        self.update_db()

        return True


class TeamGameStatsImport:
    def __init__(self, game_id):
        self.game_id = game_id
        self.json = {}
        self.table_columns = ['gameId', 'category', 'awayValue', 'homeValue']
        self.team_game_stats_df = pd.DataFrame()
        self.query_db()
        self.team_game_stats_df = self.team_game_stats_df.reindex(columns=self.table_columns)

    def update_db(self):
        team_game_stats_found = 0
        if self.team_game_stats_df.size > 0:
            team_game_stats_found = 1

            engine = nhlpd.dba_import_login()
            sql = "insert into team_game_stats_import (gameId, category, awayValue, homeValue) values " \
                  "(:gameId, :category, :awayValue, :homeValue)"
            params = self.team_game_stats_df.to_dict('records')
            with engine.connect() as conn:
                conn.execute(text(sql), parameters=params)

        log = nhlpd.GamesImportLog(game_id=self.game_id, team_game_stats_found=team_game_stats_found)
        log.insert_db()

        return True

    def clear_db(self):
        engine = nhlpd.dba_import_login()
        sql = "delete from team_game_stats_import where gameId = " + str(self.game_id)
        with engine.connect() as conn:
            conn.execute(text(sql))

        return True

    def query_db(self):
        engine = nhlpd.dba_import_login()
        sql = "select gameId, category, awayValue, homeValue from team_game_stats_import where gameId = " + \
              str(self.game_id)
        team_game_stats_df = pd.read_sql_query(sql, engine)
        engine.dispose()

        if team_game_stats_df.size > 0:
            team_game_stats_df = team_game_stats_df.reindex(columns=self.table_columns)
            team_game_stats_df.infer_objects().fillna('', inplace=True)
            self.team_game_stats_df = team_game_stats_df

        return True

    def query_nhl(self):
        team_game_stats_df = pd.json_normalize(self.json)
        team_game_stats_df.insert(0, 'gameId', self.game_id)

        if team_game_stats_df.size > 0:
            team_game_stats_df = team_game_stats_df.reindex(columns=self.table_columns)
            team_game_stats_df.infer_objects().fillna('', inplace=True)
            self.team_game_stats_df = team_game_stats_df

        return True

    def query_nhl_update_db(self):
        self.query_nhl()
        self.clear_db()
        self.update_db()

        return True


class RosterSpotsImport:
    def __init__(self, game_id):
        self.game_id = game_id
        self.json = {}
        self.table_columns = ['gameId', 'teamId', 'playerId', 'sweaterNumber', 'positionCode', 'headshot',
                              'firstName.default', 'lastName.default']
        self.roster_spots_df = pd.DataFrame()
        self.query_db()
        self.roster_spots_df = self.roster_spots_df.reindex(columns=self.table_columns)

    def update_db(self):
        roster_spots_found = 0
        if self.roster_spots_df.size > 0:
            roster_spots_found = 1

            engine = nhlpd.dba_import_login()
            sql = "insert into roster_spots_import (gameId, teamId, playerId, sweaterNumber, positionCode, " \
                  "headshot,`firstName`,`lastName`) values (:gameId, :teamId, :playerId, :sweaterNumber, " \
                  ":positionCode, :headshot, :firstNamedefault, :lastNamedefault)"
            roster_spots_df = self.roster_spots_df
            roster_spots_df.columns = roster_spots_df.columns.str.replace('.', '')
            roster_spots_df.fillna(0, inplace=True)
            params = roster_spots_df.to_dict('records')
            with engine.connect() as conn:
                conn.execute(text(sql), parameters=params)

        log = nhlpd.GamesImportLog(game_id=self.game_id, roster_spots_found=roster_spots_found)
        log.insert_db()

        return True

    def clear_db(self):
        engine = nhlpd.dba_import_login()
        sql = "delete from roster_spots_import where gameId = " + str(self.game_id)
        with engine.connect() as conn:
            conn.execute(text(sql))

        return True

    def query_db(self):
        engine = nhlpd.dba_import_login()
        sql = "select gameId, teamId, playerId, sweaterNumber, positionCode, headshot, `firstName`, `lastName` from " \
              "roster_spots_import where gameId = " + str(self.game_id)
        roster_spots_df = pd.read_sql_query(sql, engine)
        engine.dispose()

        if roster_spots_df.size > 0:
            roster_spots_df = roster_spots_df.reindex(columns=self.table_columns)
            roster_spots_df.infer_objects().fillna('', inplace=True)
            self.roster_spots_df = roster_spots_df

        return True

    def query_nhl(self):
        roster_spots_df = pd.json_normalize(self.json)
        roster_spots_df.insert(0, 'gameId', self.game_id)

        if roster_spots_df.size > 0:
            roster_spots_df = roster_spots_df.reindex(columns=self.table_columns)
            roster_spots_df.fillna(0, inplace=True)
            self.roster_spots_df = roster_spots_df

        return True

    def query_nhl_update_db(self):
        self.query_nhl()
        self.clear_db()
        self.update_db()

        return True


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

            engine = nhlpd.dba_import_login()
            sql = "insert into plays_import (gameId, eventId, `periodDescriptor.number`, " \
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

        log = nhlpd.GamesImportLog(game_id=self.game_id, plays_found=plays_found)
        log.insert_db()

        return True

    def clear_db(self):
        engine = nhlpd.dba_import_login()
        sql = "delete from plays_import where gameId = " + str(self.game_id)
        with engine.connect() as conn:
            conn.execute(text(sql))

        return True

    def query_db(self):
        engine = nhlpd.dba_import_login()
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
              "from plays_import where gameId = " + str(self.game_id)
        plays_df = pd.read_sql_query(sql, engine)
        engine.dispose()

        if plays_df.size > 0:
            plays_df = plays_df.reindex(columns=self.table_columns)
            plays_df.infer_objects().fillna('', inplace=True)
            self.plays_df = plays_df

        return True

    def query_nhl(self):
        plays_df = pd.json_normalize(self.json)
        plays_df.insert(0, 'gameId', self.game_id)

        if plays_df.size > 0:
            plays_df = plays_df.reindex(columns=self.table_columns)
            plays_df.fillna(0, inplace=True)
            self.plays_df = plays_df

        return True

    def query_nhl_update_db(self):
        self.query_nhl()
        self.clear_db()
        self.update_db()

        return True


class TvBroadcastsImport:
    def __init__(self, game_id):
        self.game_id = game_id
        self.json = {}
        self.table_columns = ['gameId', 'broadcastId', 'market', 'countryCode', 'network', 'sequenceNumber']
        self.tv_broadcasts_df = pd.DataFrame()
        self.query_db()
        self.tv_broadcasts_df = self.tv_broadcasts_df.reindex(columns=self.table_columns)

    def update_db(self):
        tv_broadcasts_found = 0
        if self.tv_broadcasts_df.size > 0:
            tv_broadcasts_found = 1

            engine = nhlpd.dba_import_login()
            sql = "insert into tv_broadcasts_import (gameId, broadcastId, market, countryCode, network, " \
                  "sequenceNumber) values (:gameId, :broadcastId, :market, :countryCode, :network, :sequenceNumber)"
            params = self.tv_broadcasts_df.to_dict('records')
            with engine.connect() as conn:
                conn.execute(text(sql), params)

        log = nhlpd.GamesImportLog(game_id=self.game_id, tv_broadcasts_found=tv_broadcasts_found)
        log.insert_db()

        return True

    def clear_db(self):
        engine = nhlpd.dba_import_login()
        sql = "delete from tv_broadcasts_import where gameId = " + str(self.game_id)
        with engine.connect() as conn:
            conn.execute(text(sql))

        return True

    def query_db(self):
        engine = nhlpd.dba_import_login()
        sql = "select gameId, broadcastId, market, countryCode, network, sequenceNumber from tv_broadcasts_import " \
              "where gameId = " + str(self.game_id)
        tv_broadcasts_df = pd.read_sql_query(sql, engine)
        engine.dispose()

        if tv_broadcasts_df.size > 0:
            tv_broadcasts_df = tv_broadcasts_df.reindex(columns=self.table_columns)
            tv_broadcasts_df.infer_objects().fillna('', inplace=True)
            self.tv_broadcasts_df = tv_broadcasts_df

        return True

    def query_nhl(self):
        tv_broadcasts_df = pd.json_normalize(self.json)
        tv_broadcasts_df.rename(columns={"id": "broadcastId"}, inplace=True)
        tv_broadcasts_df.insert(0, 'gameId', self.game_id)

        if tv_broadcasts_df.size > 0:
            tv_broadcasts_df = tv_broadcasts_df.reindex(columns=self.table_columns)
            tv_broadcasts_df.infer_objects().fillna('', inplace=True)
            self.tv_broadcasts_df = tv_broadcasts_df

        return True

    def query_nhl_update_db(self):
        self.query_nhl()
        self.clear_db()
        self.update_db()

        return True


class GameCenterImport:
    def __init__(self, game_id):
        self.game_id = game_id
        self.pbp_json = {}
        self.rr_json = {}
        self.pbp_table_columns = ['gameId', 'season', 'gameType', 'limitedScoring', 'gameDate', 'venue.default',
                                  'venueLocation.default', 'startTimeUTC', 'easternUTCOffset', 'venueUTCOffset',
                                  'gameState', 'gameScheduleState', 'periodDescriptor.number',
                                  'periodDescriptor.periodType', 'periodDescriptor.maxRegulationPeriods',
                                  'awayTeam.id', 'awayTeam.commonName.default', 'awayTeam.abbrev', 'awayTeam.score',
                                  'awayTeam.sog', 'awayTeam.logo', 'awayTeam.placeName.default',
                                  'awayTeam.placeNameWithPreposition.default', 'homeTeam.id',
                                  'homeTeam.commonName.default', 'homeTeam.abbrev', 'homeTeam.score', 'homeTeam.sog',
                                  'homeTeam.logo', 'homeTeam.placeName.default',
                                  'homeTeam.placeNameWithPreposition.default', 'shootoutInUse', 'otInUse',
                                  'clock.timeRemaining', 'clock.secondsRemaining', 'clock.running',
                                  'clock.inIntermission', 'displayPeriod', 'maxPeriods', 'gameOutcome.lastPeriodType',
                                  'regPeriods']
        self.rr_table_columns = ['gameId', 'seasonSeriesWins.awayTeamWins', 'seasonSeriesWins.homeTeamWins',
                                 'seasonSeriesWins.neededToWin', 'gameInfo.awayTeam.headCoach.default',
                                 'gameInfo.homeTeam.headCoach.default', 'gameVideo.threeMinRecap',
                                 'linescore.totals.away', 'linescore.totals.home']
        self.game_center_pbp_df = pd.DataFrame()
        self.game_center_rr_df = pd.DataFrame()

        self.tv_broadcasts = TvBroadcastsImport(game_id=game_id)
        self.plays = PlaysImport(game_id=game_id)
        self.roster_spots = RosterSpotsImport(game_id=game_id)
        self.team_game_stats = TeamGameStatsImport(game_id=game_id)
        self.season_series = SeasonSeriesImport(game_id=game_id)
        self.referees = RefereesImport(game_id=game_id)
        self.linesmen = LinesmenImport(game_id=game_id)
        self.scratches = ScratchesImport(game_id=game_id)

        self.query_db()
        self.game_center_pbp_df = self.game_center_pbp_df.reindex(columns=self.pbp_table_columns)
        self.game_center_rr_df = self.game_center_rr_df.reindex(columns=self.rr_table_columns)

    def update_db(self):
        game_center_found = 0
        if self.game_center_pbp_df.size > 0:
            game_center_found = 1
            engine = nhlpd.dba_import_login()
            sql = "insert into game_center_import (gameId, season, gameType, limitedScoring, gameDate, " \
                  "`venue.default`, `venueLocation.default`, startTimeUTC, easternUTCOffset, venueUTCOffset, " \
                  "gameState, gameScheduleState, `periodDescriptor.number`, `periodDescriptor.periodType`, " \
                  "`periodDescriptor.maxRegulationPeriods`, `awayTeam.id`, `awayTeam.commonName.default`, " \
                  "`awayTeam.abbrev`, `awayTeam.score`, `awayTeam.sog`, `awayTeam.logo`, " \
                  "`awayTeam.placeName.default`, `awayTeam.placeNameWithPreposition.default`, `homeTeam.id`, " \
                  "`homeTeam.commonName.default`, `homeTeam.abbrev`, `homeTeam.score`, `homeTeam.sog`, " \
                  "`homeTeam.logo`, `homeTeam.placeName.default`, `homeTeam.placeNameWithPreposition.default`, " \
                  "shootoutInUse, otInUse, `clock.timeRemaining`, `clock.secondsRemaining`, `clock.running`, " \
                  "`clock.inIntermission`, displayPeriod, maxPeriods, `gameOutcome.lastPeriodType`, regPeriods) " \
                  "values (:gameId, :season, :gameType, :limitedScoring, :gameDate, :venuedefault, " \
                  ":venueLocationdefault, :startTimeUTC, :easternUTCOffset, :venueUTCOffset, :gameState, " \
                  ":gameScheduleState, :periodDescriptornumber, :periodDescriptorperiodType, " \
                  ":periodDescriptormaxRegulationPeriods, :awayTeamid, :awayTeamcommonNamedefault, :awayTeamabbrev, " \
                  ":awayTeamscore, :awayTeamsog, :awayTeamlogo, :awayTeamplaceNamedefault, " \
                  ":awayTeamplaceNameWithPrepositiondefault, :homeTeamid, :homeTeamcommonNamedefault, " \
                  ":homeTeamabbrev, :homeTeamscore, :homeTeamsog, :homeTeamlogo, :homeTeamplaceNamedefault, " \
                  ":homeTeamplaceNameWithPrepositiondefault, :shootoutInUse, :otInUse, :clocktimeRemaining, " \
                  ":clocksecondsRemaining, :clockrunning, :clockinIntermission, :displayPeriod, :maxPeriods, " \
                  ":gameOutcomelastPeriodType, :regPeriods)"
            game_center_pbp_df = self.game_center_pbp_df
            game_center_pbp_df.columns = game_center_pbp_df.columns.str.replace('.', '')
            game_center_pbp_df.fillna(0, inplace=True)
            params = game_center_pbp_df.to_dict('records')

            with engine.connect() as conn:
                conn.execute(text(sql), parameters=params)

        log = nhlpd.GamesImportLog(game_id=self.game_id, game_center_found=game_center_found)
        log.insert_db()

        if len(self.game_center_rr_df.index) > 0:
            engine = nhlpd.dba_import_login()
            sql = "insert into game_center_right_rail_import (gameId, `seasonSeriesWins.awayTeamWins`, " \
                  "`seasonSeriesWins.homeTeamWins`, `seasonSeriesWins.neededToWin`, " \
                  "`gameInfo.awayTeam.headCoach.default`, `gameInfo.homeTeam.headCoach.default`, " \
                  "`gameVideo.threeMinRecap`, `linescore.totals.away`, `linescore.totals.home`) " \
                  "values (:gameId, :seasonSeriesWinsawayTeamWins, :seasonSeriesWinshomeTeamWins, " \
                  ":seasonSeriesWinsneededToWin, :gameInfoawayTeamheadCoachdefault, " \
                  ":gameInfohomeTeamheadCoachdefault, :gameVideothreeMinRecap, :linescoretotalsaway, " \
                  ":linescoretotalshome)"
            game_center_rr_df = self.game_center_rr_df
            game_center_rr_df.columns = game_center_rr_df.columns.str.replace('.', '')
            game_center_rr_df.fillna(0, inplace=True)
            params = game_center_rr_df.to_dict('records')
            with engine.connect() as conn:
                conn.execute(text(sql), parameters=params)

        self.tv_broadcasts.update_db()
        self.plays.update_db()
        self.roster_spots.update_db()
        self.team_game_stats.update_db()
        self.season_series.update_db()
        self.referees.update_db()
        self.linesmen.update_db()
        self.scratches.update_db()

        return True

    def clear_db(self):
        engine = nhlpd.dba_import_login()
        sql = "delete from game_center_import where gameId = " + str(self.game_id)
        with engine.connect() as conn:
            conn.execute(text(sql))

        engine = nhlpd.dba_import_login()
        sql = "delete from game_center_right_rail_import where gameId = " + str(self.game_id)
        with engine.connect() as conn:
            conn.execute(text(sql))

        self.tv_broadcasts.clear_db()
        self.plays.clear_db()
        self.roster_spots.clear_db()
        self.team_game_stats.clear_db()
        self.season_series.clear_db()
        self.referees.clear_db()
        self.linesmen.clear_db()
        self.scratches.clear_db()

        return True

    def query_db(self):
        engine = nhlpd.dba_import_login()
        pbp_sql = "select gameId, season, gameType, limitedScoring, gameDate, `venue.default`, " \
                  "`venueLocation.default`, startTimeUTC, easternUTCOffset, venueUTCOffset, gameState, " \
                  "gameScheduleState, `periodDescriptor.number`, `periodDescriptor.periodType`, " \
                  "`periodDescriptor.maxRegulationPeriods`, `awayTeam.id`, `awayTeam.commonName.default`, " \
                  "`awayTeam.abbrev`, `awayTeam.score`, `awayTeam.sog`, `awayTeam.logo`, " \
                  "`awayTeam.placeName.default`, `awayTeam.placeNameWithPreposition.default`, `homeTeam.id`, " \
                  "`homeTeam.commonName.default`, `homeTeam.abbrev`, `homeTeam.score`, `homeTeam.sog`, " \
                  "`homeTeam.logo`, `homeTeam.placeName.default`, `homeTeam.placeNameWithPreposition.default`, " \
                  "shootoutInUse, otInUse, `clock.timeRemaining`, `clock.secondsRemaining`, `clock.running`, " \
                  "`clock.inIntermission`, displayPeriod, maxPeriods, `gameOutcome.lastPeriodType`, regPeriods " \
                  "from game_center_import where gameId = " + str(self.game_id)
        game_center_pbp_df = pd.read_sql_query(pbp_sql, engine)
        engine.dispose()

        if game_center_pbp_df.size > 0:
            game_center_pbp_df = game_center_pbp_df.reindex(columns=self.pbp_table_columns)
            game_center_pbp_df.infer_objects().fillna('', inplace=True)
            self.game_center_pbp_df = game_center_pbp_df

        rr_sql = "select gameId, `seasonSeriesWins.awayTeamWins`, `seasonSeriesWins.homeTeamWins`, " \
                 "`seasonSeriesWins.neededToWin`, `gameInfo.awayTeam.headCoach.default`, " \
                 "`gameInfo.homeTeam.headCoach.default`, `gameVideo.threeMinRecap`, `linescore.totals.away`, " \
                 "`linescore.totals.home` from game_center_right_rail_import where gameId = " + str(self.game_id)
        game_center_rr_df = pd.read_sql_query(rr_sql, engine)
        engine.dispose()

        if game_center_rr_df.size > 0:
            game_center_rr_df = game_center_rr_df.reindex(columns=self.pbp_table_columns)
            game_center_rr_df.fillna(0, inplace=True)
            self.game_center_rr_df = game_center_rr_df

        self.tv_broadcasts.query_db()
        self.plays.query_db()
        self.roster_spots.query_db()
        self.team_game_stats.query_db()
        self.season_series.query_db()
        self.referees.query_db()
        self.linesmen.query_db()
        self.scratches.query_db()

        return True

    def query_nhl(self):
        if self.game_id != '':
            url_prefix = 'https://api-web.nhle.com/v1/gamecenter/'

            pbp_suffix = '/play-by-play'
            pbp_query_url = "{}{}{}".format(url_prefix, self.game_id, pbp_suffix)
            self.pbp_json = nhlpd.fetch_json_data(pbp_query_url)
            game_center_pbp_df = pd.json_normalize(self.pbp_json)
            game_center_pbp_df.insert(0, 'gameId', self.game_id)

            if game_center_pbp_df.size > 0:
                game_center_pbp_df = game_center_pbp_df.reindex(columns=self.pbp_table_columns)
                game_center_pbp_df.fillna(0, inplace=True)
                self.game_center_pbp_df = game_center_pbp_df

            rr_suffix = '/right-rail'
            rr_query_url = "{}{}{}".format(url_prefix, self.game_id, rr_suffix)
            self.rr_json = nhlpd.fetch_json_data(rr_query_url)
            game_center_rr_df = pd.json_normalize(self.rr_json)
            game_center_rr_df.insert(0, 'gameId', self.game_id)

            if game_center_rr_df.size > 0:
                game_center_rr_df = game_center_rr_df.reindex(columns=self.rr_table_columns)
                game_center_rr_df.fillna(0, inplace=True)
                self.game_center_rr_df = game_center_rr_df

            # in play-by-play
            if 'tvBroadcasts' in self.pbp_json:
                self.tv_broadcasts.json = self.pbp_json['tvBroadcasts']
                self.tv_broadcasts.query_nhl()

            if 'plays' in self.pbp_json:
                self.plays.json = self.pbp_json['plays']
                self.plays.query_nhl()

            if 'rosterSpots' in self.pbp_json:
                self.roster_spots.json = self.pbp_json['rosterSpots']
                self.roster_spots.query_nhl()

            # in right-rail
            if "teamGameStats" in self.rr_json:
                self.team_game_stats.json = self.rr_json['teamGameStats']
                self.team_game_stats.query_nhl()

            if "seasonSeries" in self.rr_json:
                self.season_series.json = self.rr_json['seasonSeries']
                self.season_series.query_nhl()

            if "referees" in self.rr_json['gameInfo']:
                self.referees.json = self.rr_json['gameInfo']['referees']
                self.referees.query_nhl()

            if "linesmen" in self.rr_json['gameInfo']:
                self.linesmen.json = self.rr_json['gameInfo']['linesmen']
                self.linesmen.query_nhl()

            if "scratches" in self.rr_json['gameInfo']['awayTeam']:
                self.scratches.json = self.rr_json['gameInfo']['awayTeam']['scratches'] + \
                                      self.rr_json['gameInfo']['homeTeam']['scratches']
                self.scratches.query_nhl()

        return True

    def query_nhl_update_db(self):
        self.query_nhl()
        self.clear_db()
        self.update_db()

        return True
