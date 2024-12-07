from datetime import datetime, timedelta
import pandas as pd
from .mysql_db import db_import_login


class Scheduler:
    def __init__(self):
        self.current_time = datetime.now()

        self.table_log_df = pd.DataFrame()
        self.game_log_df = pd.DataFrame()
        self.player_log_df = pd.DataFrame()

        self.queryDBforTables()
        self.queryDBforGames()
        self.queryDBforPlayers()

    def queryDBforTables(self):
        cursor, db = db_import_login()

        sql = "select tableName, max(lastDateUpdated) as lastDateUpdated from table_update_log where updateFound = 1 " \
              "group by tableName"
        self.table_log_df = pd.read_sql(sql, db)

        db.commit()
        cursor.close()
        db.close()

        return True

    def queryDBforGames(self):
        cursor, db = db_import_login()

        sql = "select a.gameId, a.lastDateUpdated, a.gameFound, a.gameCenterFound, a.tvBroadcastsFound, " \
              "a.playsFound, a.rosterSpotsFound, a.teamGameStatsFound, a.seasonSeriesFound, " \
              "a.linescoreByPeriodFound, a.refereesFound, a.linesmenFound, a.scratchesFound, a.shiftsFound " \
              "from games_import_log as a join (select gameId, max(lastDateUpdated) as lastDateUpdated " \
              "from games_import_log group by gameId) as b on a.gameId = b.gameId and " \
              "a.lastDateUpdated = b.lastDateUpdated"
        self.game_log_df = pd.read_sql(sql, db)

        db.commit()
        cursor.close()
        db.close()

        return True

    def queryDBforPlayers(self):
        cursor, db = db_import_login()

        sql = "select a.playerId, a.lastDateUpdated, a.playerFound, a.playerBioFound, a.careerTotalsFound, " \
              "a.seasonTotalsFound, a.awardsFound from player_import_log as a join (select playerId, " \
              "max(lastDateUpdated) as lastDateUpdated from player_import_log group by playerId) as b on " \
              "a.playerId = b.playerId and a.lastDateUpdated = b.lastDateUpdated"
        self.player_log_df = pd.read_sql(sql, db)

        db.commit()
        cursor.close()
        db.close()

        return True

    def checkTeams(self):
        check_bool = False
        # if there's no record in the log
        if "teams_import" not in self.table_log_df['tableName'].values:
            check_bool = True

        # if it's been six months since the last check
        junkvar = self.current_time - self.table_log_df.loc[self.table_log_df['tableName'] == "teams_import",
                                                            'lastDateUpdated'].item()

        timevar = timedelta(days=180)

        if junkvar > timevar:
            print('yis')
        else:
            print('nay')


        if self.table_log_df.loc[self.table_log_df['tableName'] == "teams_import", 'lastDateUpdated'].item():
            print("run")
        else:
            print("don't run")

        return check_bool

    def checkSeasons(self):
        check_bool = False
        # if there's no record in the log

        # if there's a new team

        # if we should expect a new season based on the calendar month

    def checkGames(self):
        season = ''
        games = []
        check_bool = False
        # if there's no record in the log (all seasons)

        # if there's a new season (new season)

        # if we're in a current season & it has been a month (current season)

        # if we're in the post-season (current season)

    def checkGameCenters(self):
        check_bool = False
        # if there's are games in the games_import_log table

    def checkRosters(self):
        seasons = []
        check_bool = False
        # if there's no record in the log (all seasons)

        # if there's a new season (new season)

        # if there's a new team (max season)

        # if it has been a month since the last check (max season)

    def checkPlayers(self):
        players = []
        check_bool = False
        # if there's no record in the log (all players)

        # if there are players who haven't been checked (all players)

        # if there are games that have been played since the last check
