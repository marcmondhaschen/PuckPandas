import pandas as pd
import puckpandas
from sqlalchemy import text


class GamesImport:
    def __init__(self, team_id, season_id):
        self.team_id = team_id
        self.season_id = season_id
        self.teams = puckpandas.TeamsImport()
        self.table_columns = ['gameId', 'seasonId', 'gameType', 'gameDate', 'venue', 'neutralSite', 'startTimeUTC',
                              'venueUTCOffset', 'venueTimezone', 'gameState', 'gameScheduleState', 'awayTeam',
                              'awayTeamSplitSquad', 'awayTeamScore', 'homeTeam', 'homeTeamSplitSquad', 'homeTeamScore',
                              'periodType', 'gameOutcome', 'seriesStatus.round', 'seriesStatus.seriesAbbrev',
                              'seriesStatus.seriesTitle', 'seriesStatus.seriesLetter', 'seriesStatus.neededToWin',
                              'seriesStatus.topSeedWins', 'seriesStatus.bottomSeedWins',
                              'seriesStatus.gameNumberOfSeries']
        self.games_df = pd.DataFrame()
        self.query_db()
        self.games_df = self.games_df.reindex(columns=self.table_columns)

    def update_db(self):
        games_found = 0
        if self.games_df.size > 0:
            games_found = 1
            engine = puckpandas.dba_import_login()
            sql = "insert into puckpandas_import.games_import (gameId, seasonId, gameType, gameDate, venue, " \
                  "neutralSite, " \
                  "startTimeUTC, venueUTCOffset, venueTimezone, gameState, gameScheduleState, awayTeam, " \
                  "awayTeamSplitSquad, awayTeamScore, homeTeam, homeTeamSplitSquad, homeTeamScore, " \
                  "periodType, gameOutcome, `seriesStatus.round`, `seriesStatus.seriesAbbrev`, " \
                  "`seriesStatus.seriesTitle`, `seriesStatus.seriesLetter`, `seriesStatus.neededToWin`, " \
                  "`seriesStatus.topSeedWins`, `seriesStatus.bottomSeedWins`, `seriesStatus.gameNumberOfSeries`) " \
                  "values (:gameId, :seasonId, :gameType, :gameDate, :venue, :neutralSite, :startTimeUTC, " \
                  ":venueUTCOffset, :venueTimezone, :gameState, :gameScheduleState, :awayTeam, " \
                  ":awayTeamSplitSquad, :awayTeamScore, :homeTeam, :homeTeamSplitSquad, :homeTeamScore, " \
                  ":periodType, :gameOutcome, :seriesStatusround, :seriesStatusseriesAbbrev, " \
                  ":seriesStatusseriesTitle, :seriesStatusseriesLetter, :seriesStatusneededToWin, " \
                  ":seriesStatustopSeedWins, :seriesStatusbottomSeedWins, :seriesStatusgameNumberOfSeries)"
            games_transform_df = self.games_df
            games_transform_df.columns = games_transform_df.columns.str.replace('.', '')
            params = games_transform_df.to_dict('records')

            with engine.connect() as conn:
                conn.execute(text(sql), parameters=params)

            for index, row in games_transform_df.iterrows():
                game_log = puckpandas.GamesImportLog(row['gameId'], game_found=1)
                game_log.insert_db()

        season_log = puckpandas.SeasonsImportLog(team_id=self.team_id, season_id=self.season_id, games_found=games_found)
        season_log.insert_db()

        return True

    def clear_db(self):
        if self.team_id != '' and self.season_id != '':
            engine = puckpandas.dba_import_login()
            sql = "delete from puckpandas_import.games_import where gameId > 0" + " and (homeTeam = " + \
                  str(self.team_id) + " or awayTeam = " + str(self.team_id) + ")" + " and seasonId = '" + \
                  str(self.season_id) + "'"
            with engine.connect() as conn:
                conn.execute(text(sql))
            engine.dispose()

        return True

    def query_db(self):
        engine = puckpandas.dba_import_login()
        sql = "select gameId, seasonId, gameType, gameDate, venue, neutralSite, startTimeUTC, venueUTCOffset, " \
              "venueTimezone, gameState, gameScheduleState, awayTeam, awayTeamSplitSquad, awayTeamScore, homeTeam, " \
              "homeTeamSplitSquad, homeTeamScore, periodType, gameOutcome, `seriesStatus.round`, " \
              "`seriesStatus.seriesAbbrev`, `seriesStatus.seriesTitle`, `seriesStatus.seriesLetter`, " \
              "`seriesStatus.neededToWin`, `seriesStatus.topSeedWins`, `seriesStatus.bottomSeedWins`, " \
              "`seriesStatus.gameNumberOfSeries` from puckpandas_import.games_import where gameId > 0 and " \
              "(homeTeam = " + str(self.team_id) + " or awayTeam = " + str(self.team_id) + ") and seasonId = '" + \
               str(self.season_id) + "'"
        games_df = pd.read_sql_query(sql, engine)
        engine.dispose()

        if games_df.size > 0:
            games_df = games_df.reindex(columns=self.table_columns)
            games_df.infer_objects().fillna('', inplace=True)
            games_df.drop_duplicates(inplace=True)
            self.games_df = games_df

        return self.games_df

    def query_api(self):
        # each page call is a complete season for a given team
        tri_code = self.teams.tri_code_from_team_id(team_id=self.team_id)

        base_url = 'https://api-web.nhle.com/v1/club-schedule-season/'
        query_string = "{}{}/{}".format(base_url, tri_code, self.season_id)
        json_data = puckpandas.fetch_json_data(query_string)

        if 'games' in json_data:
            games_df = pd.json_normalize(json_data, record_path=['games'])
            if 'tvBroadcasts' in games_df:
                games_df.drop(columns='tvBroadcasts', inplace=True)

            games_df.rename(columns={'id': 'gameId', 'season': 'seasonId', 'venue.default': 'venue',
                                     'awayTeam.id': 'awayTeam', 'awayTeam.awaySplitSquad': 'awayTeamSplitSquad',
                                     'awayTeam.score': 'awayTeamScore', 'homeTeam.id': 'homeTeam',
                                     'homeTeam.homeSplitSquad': 'homeTeamSplitSquad', 'homeTeam.score': 'homeTeamScore',
                                     'periodDescriptor.periodType': 'periodType',
                                     'gameOutcome.lastPeriodType': 'gameOutcome'}, inplace=True)
            games_df = games_df.reindex(columns=self.table_columns)
            games_df.drop(columns=['homeTeam.commonName.fr', 'awayTeam.commonName.fr'], errors='ignore')
            games_df.fillna(0, inplace=True)

            if games_df.size > 0:
                self.games_df = games_df

        return self.games_df

    def query_api_update_db(self):
        # For this object, this pattern has the side effect of deleting duplicate gameIds in the games_import table.
        # Each game is presented twice by the API - once for each opposing team. the
        # clear method will drop games from a team about to be imported, removing their impending duplication on import_feed
        # but leaving behind all the previous competitors' matches that didn't involve them.
        self.query_api()
        self.clear_db()
        self.update_db()

        return True


class Venues:
    def __init__(self):
        self.table_columns = ['venueId', 'venue']
        self.venues_df = pd.DataFrame()
        self.query_db()
        self.venues_df = self.venues_df.reindex(columns=self.table_columns)

    def update_db(self):
        if self.venues_df.size > 0:
            engine = puckpandas.dba_prod_login()
            sql = "insert into `puckpandas`.`venues` (venue) select distinct venue as venueName from "\
                  "puckpandas_import.games_import order by venue"

            with engine.connect() as conn:
                conn.execute(text(sql))

        return True

    @staticmethod
    def clear_db():
            engine = puckpandas.dba_prod_login()
            sql = "delete from puckpandas.venues"

            with engine.connect() as conn:
                conn.execute(text(sql))
            engine.dispose()

            return True

    def query_db(self):
        engine = puckpandas.dba_prod_login()
        sql = "select venueId, venue from puckpandas.venues"
        venues_df = pd.read_sql_query(sql, engine)
        engine.dispose()

        if venues_df.size > 0:
            venues_df = venues_df.reindex(columns=self.table_columns)
            venues_df.infer_objects().fillna('', inplace=True)
            venues_df.drop_duplicates(inplace=True)
            self.venues_df = venues_df

        return self.venues_df


class Games:
    def __init__(self):
        self.table_columns = ['gameId', 'seasonId', 'gameType', 'gameDate', 'venueId', 'startTimeUTC',
                              'startTimeVenue', 'awayTeam', 'homeTeam']
        self.games_df = pd.DataFrame()
        self.query_db()
        self.games_df = self.games_df.reindex(columns=self.table_columns)

    def update_db(self):
        if self.games_df.size > 0:
            engine = puckpandas.dba_prod_login()
            sql = "insert into puckpandas.games (gameId, seasonId, gameType, gameDate, venueId, startTimeUTC, " \
                  "startTimeVenue, awayTeam, homeTeam) select a.gameId, a.seasonId, a.gameType, a.gameDate, " \
                  "b.venueId, a.startTimeUTC, date_add(a.startTimeUTC, INTERVAL time_to_sec(left(a.venueUTCOffset, " \
                  "locate(':', a.venueUTCOffset)+2)) second) as startTimeVenue, a.awayTeam, a.homeTeam from " \
                  "puckpandas_import.games_import as a join puckpandas.venues as b on a.venue = b.venue"

            with engine.connect() as conn:
                conn.execute(text(sql))

        return True

    @staticmethod
    def clear_db():
        engine = puckpandas.dba_prod_login()
        sql = "delete from puckpandas.games"

        with engine.connect() as conn:
            conn.execute(text(sql))
        engine.dispose()

        return True

    def query_db(self):
        engine = puckpandas.dba_prod_login()
        sql = "select gameId, seasonId, gameType, gameDate, venueId, startTimeUTC, startTimeVenue, awayTeam, " \
              "homeTeam from puckpandas.games"
        games_df = pd.read_sql_query(sql, engine)
        engine.dispose()

        if games_df.size > 0:
            games_df = games_df.reindex(columns=self.table_columns)
            games_df.infer_objects().fillna('', inplace=True)
            games_df.drop_duplicates(inplace=True)
            self.games_df = games_df

        return self.games_df


class GameScores:
    def __init__(self):
        self.table_columns = ['gameId', 'periodType', 'gameOutcome', 'awayTeam', 'awayScore', 'awayLineScore',
                              'awaySOG', 'homeTeam', 'homeScore', 'homeLineScore', 'homeSOG']
        self.game_scores_df = pd.DataFrame()
        self.query_db()
        self.game_scores_df = self.game_scores_df.reindex(columns=self.table_columns)
        self.current_season = puckpandas.SeasonsImport.current_season()

    def update_db(self):
        if self.game_scores_df.size > 0:
            engine = puckpandas.dba_prod_login()
            sql = "insert into puckpandas.game_scores (gameId, periodType, gameOutcome, awayTeam, awayScore, " \
                  "awayLineScore, awaySOG, homeTeam, homeScore, homeLineScore, homeSOG) select a.gameId, " \
                  "a.periodType, a.gameOutcome, a.awayTeam, a.awayTeamScore as awayScore, c.`linescore.totals.away` " \
                  "as awayLineScore, b.`awayTeam.sog` as awaySOG, a.homeTeam, a.homeTeamScore as homeScore, " \
                  "c.`linescore.totals.home` as homeLineScore, b.`homeTeam.sog` as homeSOG from " \
                  "puckpandas_import.games_import as a join puckpandas_import.game_center_import as b on " \
                  "a.gameId = b.gameId join puckpandas_import.game_center_right_rail_import as c on a.gameId = " \
                  "c.gameId where a.seasonId = " + str(self.current_season)

            with engine.connect() as conn:
                conn.execute(text(sql))

        return True

    @staticmethod
    def clear_db():
        engine = puckpandas.dba_prod_login()
        sql = "delete from puckpandas.game_scores"

        with engine.connect() as conn:
            conn.execute(text(sql))
        engine.dispose()

        return True

    def query_db(self):
        engine = puckpandas.dba_prod_login()
        sql = ""
        game_scores_df = pd.read_sql_query(sql, engine)
        engine.dispose()

        if game_scores_df.size > 0:
            game_scores_df = game_scores_df.reindex(columns=self.table_columns)
            game_scores_df.infer_objects().fillna('', inplace=True)
            game_scores_df.drop_duplicates(inplace=True)
            self.game_scores_df = game_scores_df

        return self.game_scores_df


class GameProgress:
    def __init__(self):
        self.table_columns = ['gameId', 'gameState', 'gameScheduleState', 'periodNumber', 'periodType',
                              'secondsRemaining', 'clockRunning', 'inIntermission', 'maxPeriods', 'lastPeriodType',
                              'regPeriods']
        self.game_progress_df = pd.DataFrame()
        self.query_db()
        self.game_progress_df = self.game_progress_df.reindex(columns=self.table_columns)
        self.current_season = puckpandas.SeasonsImport.current_season()

    def update_db(self):
        if self.game_progress_df.size > 0:
            engine = puckpandas.dba_prod_login()
            sql = "insert into puckpandas.game_progress (gameId, gameState, gameScheduleState, periodNumber, " \
                  "periodType, secondsRemaining, clockRunning, inIntermission, maxPeriods, lastPeriodType, " \
                  "regPeriods) select a.gameId, a.gameState, a.gameScheduleState, b.`periodDescriptor.number` as " \
                  "periodNumber, b.`periodDescriptor.periodType` as periodType, b.`clock.secondsRemaining` as " \
                  "secondsRemaining, b.`clock.running` as clockRunning, b.`clock.inIntermission` as inIntermission, " \
                  "b.maxPeriods, b.`gameOutcome.lastPeriodType` as lastPeriodType, b.regPeriods from " \
                  "puckpandas_import.games_import as a join puckpandas_import.game_center_import as b on " \
                  "a.gameId = b.gameId where a.seasonId = " + str(self.current_season)

            with engine.connect() as conn:
                conn.execute(text(sql))

        return True

    @staticmethod
    def clear_db():
        engine = puckpandas.dba_prod_login()
        sql = "delete from puckpandas.game_progress"

        with engine.connect() as conn:
            conn.execute(text(sql))
        engine.dispose()

        return True

    def query_db(self):
        engine = puckpandas.dba_prod_login()
        sql = ""
        game_progress_df = pd.read_sql_query(sql, engine)
        engine.dispose()

        if game_progress_df.size > 0:
            game_progress_df = game_progress_df.reindex(columns=self.table_columns)
            game_progress_df.infer_objects().fillna('', inplace=True)
            game_progress_df.drop_duplicates(inplace=True)
            self.game_progress_df = game_progress_df

        return self.game_progress_df


class GameResults:
    def __init__(self):
        self.table_columns = ['resultId', 'gameId', 'gameType', 'seasonId', 'teamId', 'opponentTeamId', 'teamWin',
                              'teamOT', 'teamLoss', 'awayGame', 'awayWin', 'awayOT', 'awayLoss', 'homeGame', 'homeWin',
                              'homeOT', 'homeLoss', 'tie', 'overtime', 'awayScore', 'homeScore', 'standingPoints']
        self.game_results_df = pd.DataFrame()
        self.query_db()
        self.game_results_df = self.game_results_df.reindex(columns=self.table_columns)
        self.current_season = puckpandas.SeasonsImport.current_season()

    def update_db(self):
        if self.game_results_df.size > 0:
            engine = puckpandas.dba_prod_login()
            sql = "insert into puckpandas.game_results select concat(gameId, lpad(teamId, 2, 0)) as resultId, " \
                  "gameId, gameType, seasonId, teamId, opponentTeamId, teamWin, teamOT, teamLoss, awayGame, awayWin, " \
                  "awayOT, awayLoss, homeGame, homeWin, homeOT, homeLoss, tie, overtime, awayScore, homeScore, case " \
                  "when gameType = 2 and teamWin = 1 then 2 when gameType = 2 and overtime = 1 and teamWin = 0 then " \
                  "1 when gameType = 3 and teamWin = 1 then 1 else 0 end as standingPoints from (select gameId, " \
                  "gameType, seasonId, teamId, opponentTeamId, awayGame, homeGame, case when (awayGame = 1 and " \
                  "awayWin = 1) or (homeGame = 1 and homeWin = 1) then 1 else 0 end as teamWin, case when " \
                  "(awayGame = 1 and awayWin = 0 and overtime = 1) or (homeGame = 1 and homeWin = 0 and " \
                  "overtime = 1) then 1 else 0 end as teamOT, case when (awayGame = 1 and awayWin = 0 and " \
                  "overtime = 0) or (homeGame = 1 and homeWin = 0 and overtime = 0) then 1 else 0 end as teamLoss, " \
                  "case when awayGame = 1 and awayWin = 1 then 1 else 0 end as awayWin, case when awayGame = 1 and " \
                  "awayWin = 0 and overtime = 1 then 1 else 0 end as awayOT, case when awayGame = 1 and awayWin = 0 " \
                  "and overtime = 0 then 1 else 0 end as awayLoss, case when homeGame = 1 and homeWin = 1 then 1 " \
                  "else 0 end as homeWin, case when homeGame = 1 and homeWin = 0 and overtime = 1 then 1 else 0 end " \
                  "as homeOT, case when homeGame = 1 and homeWin = 0 and overtime = 0 then 1 else 0 end as homeLoss, " \
                  "tie, overtime, awayScore, homeScore from (select g.gameId, g.gameType, g.seasonId, g.awayTeam as " \
                  "teamId, g.homeTeam as opponentTeamId, 1 as awayGame, 0 as homeGame, case when s.awayScore > " \
                  "s.homeScore then 1 else 0 end as awayWin, case when s.awayScore < s.homeScore then 1 else 0 end " \
                  "as homeWin, case when s.awayScore = s.homeScore then 1 else 0 end as tie, s.awayScore, " \
                  "s.homeScore, case when s.periodType in ('OT', 'SO') then 1 else 0 end as overtime from " \
                  "puckpandas.games as g join puckpandas.game_scores as s on g.gameId = s.gameId join " \
                  "puckpandas.game_progress as p on g.gameId = p.gameId where g.gameType in (2, 3) and " \
                  "s.periodType in ('OT', 'REG', 'SO') and p.gameState in ('FINAL', 'OFF') and g.seasonId = " \
                  + str(self.current_season) + " union select g.gameId, g.gameType, g.seasonId, g.homeTeam as " \
                  "teamId, g.awayTeam as opponentTeamId, 0 as awayGame, 1 as homeGame, case when s.awayScore > " \
                  "s.homeScore then 1 else 0 end as awayWin, case when s.awayScore < s.homeScore then 1 else 0 end as "\
                  "homeWin, case when s.awayScore = s.homeScore then 1 else 0 end as tie, s.awayScore, s.homeScore, " \
                  "'case when s.periodType in ('OT', 'SO') then 1 else 0 end as overtime from puckpandas.games " \
                  "as g join puckpandas.game_scores as s on g.gameId = s.gameId join " \
                  "puckpandas.game_progress as p on g.gameId = p.gameId where g.gameType in (2, 3) and " \
                  "s.periodType in ('OT', 'REG', 'SO') and p.gameState in ('FINAL', 'OFF') and g.seasonId = " \
                  + str(self.current_season) + ") as a) as b"

            with engine.connect() as conn:
                conn.execute(text(sql))

        return True

    @staticmethod
    def clear_db():
        engine = puckpandas.dba_prod_login()
        sql = "delete from puckpandas.game_results"

        with engine.connect() as conn:
            conn.execute(text(sql))
        engine.dispose()

        return True

    def query_db(self):
        engine = puckpandas.dba_prod_login()
        sql = ""
        game_results_df = pd.read_sql_query(sql, engine)
        engine.dispose()

        if game_results_df.size > 0:
            game_results_df = game_results_df.reindex(columns=self.table_columns)
            game_results_df.infer_objects().fillna('', inplace=True)
            game_results_df.drop_duplicates(inplace=True)
            self.game_results_df = game_results_df

        return self.game_results_df
