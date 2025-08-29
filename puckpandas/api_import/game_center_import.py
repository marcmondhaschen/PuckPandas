import pandas as pd
import puckpandas as pp
from sqlalchemy import text


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

        self.tv_broadcasts = pp.TvBroadcastsImport(game_id=game_id)
        self.plays = pp.PlaysImport(game_id=game_id)
        self.roster_spots = pp.RosterSpotsImport(game_id=game_id)
        self.team_game_stats = pp.TeamGameStatsImport(game_id=game_id)
        self.season_series = pp.SeasonSeriesImport(game_id=game_id)
        self.referees = pp.RefereesImport(game_id=game_id)
        self.linesmen = pp.LinesmenImport(game_id=game_id)
        self.scratches = pp.ScratchesImport(game_id=game_id)

        self.query_db()
        self.game_center_pbp_df = self.game_center_pbp_df.reindex(columns=self.pbp_table_columns)
        self.game_center_rr_df = self.game_center_rr_df.reindex(columns=self.rr_table_columns)

    def update_db(self):
        game_center_found = 0
        if self.game_center_pbp_df.size > 0:
            game_center_found = 1
            engine = pp.dba_import_login()
            sql = "insert into puckpandas_import.game_center_import (gameId, season, gameType, limitedScoring, " \
                  "gameDate, `venue.default`, `venueLocation.default`, startTimeUTC, easternUTCOffset, " \
                  "venueUTCOffset, gameState, gameScheduleState, `periodDescriptor.number`, " \
                  "`periodDescriptor.periodType`, `periodDescriptor.maxRegulationPeriods`, `awayTeam.id`, " \
                  "`awayTeam.commonName.default`, `awayTeam.abbrev`, `awayTeam.score`, `awayTeam.sog`, " \
                  "`awayTeam.logo`, `awayTeam.placeName.default`, `awayTeam.placeNameWithPreposition.default`, " \
                  "`homeTeam.id`, `homeTeam.commonName.default`, `homeTeam.abbrev`, `homeTeam.score`, `homeTeam.sog`, "\
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

        log = pp.GamesImportLog(game_id=self.game_id, game_center_found=game_center_found)
        log.insert_db()

        if len(self.game_center_rr_df.index) > 0:
            engine = pp.dba_import_login()
            sql = "insert into puckpandas_import.game_center_right_rail_import (gameId, " \
                  "`seasonSeriesWins.awayTeamWins`, " \
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
        engine = pp.dba_import_login()
        sql = "delete from puckpandas_import.game_center_import where gameId = " + str(self.game_id)
        with engine.connect() as conn:
            conn.execute(text(sql))

        engine = pp.dba_import_login()
        sql = "delete from puckpandas_import.game_center_right_rail_import where gameId = " + str(self.game_id)
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
        engine = pp.dba_import_login()
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
                  "from puckpandas_import.game_center_import where gameId = " + str(self.game_id)
        game_center_pbp_df = pd.read_sql_query(pbp_sql, engine)
        engine.dispose()

        if game_center_pbp_df.size > 0:
            game_center_pbp_df = game_center_pbp_df.reindex(columns=self.pbp_table_columns)
            game_center_pbp_df.infer_objects().fillna('', inplace=True)
            self.game_center_pbp_df = game_center_pbp_df

        rr_sql = "select gameId, `seasonSeriesWins.awayTeamWins`, `seasonSeriesWins.homeTeamWins`, " \
                 "`seasonSeriesWins.neededToWin`, `gameInfo.awayTeam.headCoach.default`, " \
                 "`gameInfo.homeTeam.headCoach.default`, `gameVideo.threeMinRecap`, `linescore.totals.away`, " \
                 "`linescore.totals.home` from puckpandas_import.game_center_right_rail_import where gameId = " \
                 + str(self.game_id)
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

    def query_api(self):
        if self.game_id != '':
            url_prefix = 'https://api-web.nhle.com/v1/gamecenter/'

            pbp_suffix = '/play-by-play'
            pbp_query_url = "{}{}{}".format(url_prefix, self.game_id, pbp_suffix)
            self.pbp_json = pp.fetch_json_data(pbp_query_url)
            game_center_pbp_df = pd.json_normalize(self.pbp_json)
            game_center_pbp_df.insert(0, 'gameId', self.game_id)

            if game_center_pbp_df.size > 0:
                game_center_pbp_df = game_center_pbp_df.reindex(columns=self.pbp_table_columns)
                game_center_pbp_df.fillna(0, inplace=True)
                self.game_center_pbp_df = game_center_pbp_df

            rr_suffix = '/right-rail'
            rr_query_url = "{}{}{}".format(url_prefix, self.game_id, rr_suffix)
            self.rr_json = pp.fetch_json_data(rr_query_url)
            game_center_rr_df = pd.json_normalize(self.rr_json)
            game_center_rr_df.insert(0, 'gameId', self.game_id)

            if game_center_rr_df.size > 0:
                game_center_rr_df = game_center_rr_df.reindex(columns=self.rr_table_columns)
                game_center_rr_df.fillna(0, inplace=True)
                self.game_center_rr_df = game_center_rr_df

            # in play-by-play
            if 'tvBroadcasts' in self.pbp_json:
                self.tv_broadcasts.json = self.pbp_json['tvBroadcasts']
                self.tv_broadcasts.query_api()

            if 'plays' in self.pbp_json:
                self.plays.json = self.pbp_json['plays']
                self.plays.query_api()

            if 'rosterSpots' in self.pbp_json:
                self.roster_spots.json = self.pbp_json['rosterSpots']
                self.roster_spots.query_api()

            # in right-rail
            if "teamGameStats" in self.rr_json:
                self.team_game_stats.json = self.rr_json['teamGameStats']
                self.team_game_stats.query_api()

            if "seasonSeries" in self.rr_json:
                self.season_series.json = self.rr_json['seasonSeries']
                self.season_series.query_api()

            if "referees" in self.rr_json['gameInfo']:
                self.referees.json = self.rr_json['gameInfo']['referees']
                self.referees.query_api()

            if "linesmen" in self.rr_json['gameInfo']:
                self.linesmen.json = self.rr_json['gameInfo']['linesmen']
                self.linesmen.query_api()

            if "scratches" in self.rr_json['gameInfo']['awayTeam']:
                self.scratches.json = self.rr_json['gameInfo']['awayTeam']['scratches'] + \
                                      self.rr_json['gameInfo']['homeTeam']['scratches']
                self.scratches.query_api()

        return True

    def query_api_update_db(self):
        self.query_api()
        self.clear_db()
        self.update_db()

        return True
