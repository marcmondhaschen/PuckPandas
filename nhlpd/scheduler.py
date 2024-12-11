from datetime import datetime, timedelta
import pandas as pd
import nhlpd
from .mysql_db import db_import_login
from .import_table_update_log import ImportTableUpdateLog


class Scheduler:
    def __init__(self):
        self.current_time = datetime.now()
        self.max_season_id = self.setMaxSeason()

        self.table_log_df = nhlpd.ImportTableUpdateLog()
        self.game_log_df = self.queryDBforGames()
        self.player_log_df = self.queryDBforPlayers()

    @staticmethod
    def queryDBforTables():
        cursor, db = db_import_login()

        sql = "select tableName, max(lastDateUpdated) as lastDateUpdated from table_update_log where updateFound = 1 " \
              "group by tableName"
        table_log_df = pd.read_sql(sql, db)

        db.commit()
        cursor.close()
        db.close()

        return table_log_df

    @staticmethod
    def queryDBforGames():
        cursor, db = db_import_login()

        sql = "select a.gameId, a.lastDateUpdated, a.gameFound, a.gameCenterFound, a.tvBroadcastsFound, " \
              "a.playsFound, a.rosterSpotsFound, a.teamGameStatsFound, a.seasonSeriesFound, " \
              "a.linescoreByPeriodFound, a.refereesFound, a.linesmenFound, a.scratchesFound, a.shiftsFound " \
              "from games_import_log as a join (select gameId, max(lastDateUpdated) as lastDateUpdated " \
              "from games_import_log group by gameId) as b on a.gameId = b.gameId and " \
              "a.lastDateUpdated = b.lastDateUpdated"
        game_log_df = pd.read_sql(sql, db)

        db.commit()
        cursor.close()
        db.close()

        return game_log_df

    @staticmethod
    def queryDBforPlayers():
        cursor, db = db_import_login()

        sql = "select a.playerId, a.lastDateUpdated, a.playerFound, a.playerBioFound, a.careerTotalsFound, " \
              "a.seasonTotalsFound, a.awardsFound from player_import_log as a join (select playerId, " \
              "max(lastDateUpdated) as lastDateUpdated from player_import_log group by playerId) as b on " \
              "a.playerId = b.playerId and a.lastDateUpdated = b.lastDateUpdated"
        player_log_df = pd.read_sql(sql, db)

        db.commit()
        cursor.close()
        db.close()

        return player_log_df

    @staticmethod
    def setMaxSeason():
        cursor, db = db_import_login()
        sql = "select max(seasonId) as seasonId from team_seasons_import"
        max_df = pd.read_sql(sql, db)

        db.commit()
        cursor.close()
        db.close()

        max_season_id = max_df.at[0, 'seasonId']

        return max_season_id

    def checkTeamsImport(self):
        update_interval = timedelta(days=180)
        check_bool = False
        last_update = self.table_log_df.lastUpdate(table_name="teams_import")

        # if there's no record in the log
        if last_update != '':
            check_bool = True

        # if it's been six months since the last check
        if self.current_time - last_update > update_interval:
            check_bool = True

        return check_bool

    def checkSeasonsImport(self):
        max_season_start_year = int(self.max_season_id[0:4])
        max_season_end_year = int(self.max_season_id[4:8])
        last_update = self.table_log_df.lastUpdate(table_name="team_seasons_import")

        # if there's no record in the log
        if last_update == '':
            check_bool = True

            return check_bool

        # if we are in a play season & our database has the current season we pass, otherwise run
        if self.current_time.month >= 9 and self.current_time.year == max_season_start_year:
            check_bool = False
        elif self.current_time.month < 6 and self.current_time.year == max_season_end_year:
            check_bool = False
        else:
            check_bool = True

        return check_bool

    def checkGamesImport(self):
        seasons = pd.Series()
        check_bool = False
        last_update = self.table_log_df.lastUpdate(table_name="games_import")

        # if there's no record in the log (all seasons)
        if last_update == '':
            seasons.append(99999999)
            check_bool = True

            return {check_bool, seasons}

        # if there's a new season (new season)
        cursor, db = db_import_login()
        sql = "select a.seasonId, count(b.gameId) as gameCount from team_seasons_import as a left join " \
              "games_import as b on a.seasonId = b.seasonId group by a.seasonId having gameCount = 0"
        new_seasons_df = pd.read_sql(sql, db)

        db.commit()
        cursor.close()
        db.close()

        if seasons.len() > 0:
            seasons = new_seasons_df['seasonId']
            check_bool = True

            return {check_bool, seasons}

        # if we're in the post-season (current season)
        if 4 <= self.current_time.month <= 6:
            check_bool = True
            seasons.append(self.max_season_id)

        return {check_bool, seasons}

    @staticmethod
    def checkGameCentersImport():
        games = pd.Series()
        check_bool = False

        # if there are unchecked games in the games_import_log table
        cursor, db = db_import_login()

        sql = "select a.gameId from games_import as a left join games_import_log as b on a.gameId = b.gameId " \
              "where b.lastDateUpdated is null"
        games_to_check_df = pd.read_sql(sql, db)
        games_to_check = games_to_check_df['gameId']

        if games_to_check.len() > 0:
            games = games_to_check
            check_bool = True

        return {check_bool, games}

    def checkRostersImport(self):
        update_interval = timedelta(days=30)
        seasons = pd.Series()
        check_bool = False
        last_update = self.table_log_df.lastUpdate(table_name="rosters_import")

        # if there's no record in the log (all seasons)
        if last_update == '':
            seasons = pd.Series(99999999)
            check_bool = True
            return {check_bool, seasons}

        # if there's a new season in the DB (new seasons)
        cursor, db = db_import_login()
        sql = "select a.seasonId, count(b.playerId) as playerCount from team_seasons_import as a left join " \
              "rosters_import as b on a.seasonId = b.seasonId group by a.seasonId having playerCount = 0"
        new_seasons_df = pd.read_sql(sql, db)

        db.commit()
        cursor.close()
        db.close()

        if seasons.len() > 0:
            seasons = new_seasons_df['seasonId']
            check_bool = True

            return {check_bool, seasons}

        # if there's a new team (max season)
        cursor, db = db_import_login()
        sql = "select a.triCode, count(b.playerId) as playerCount from team_seasons_import as a " \
              "left join rosters_import as b on a.triCode = b.triCode group by a.triCode having playerCount = 0"
        new_seasons_df = pd.read_sql(sql, db)

        db.commit()
        cursor.close()
        db.close()

        seasons = new_seasons_df['seasonId']

        if seasons.len() > 0:
            seasons = pd.Series(self.max_season_id)
            check_bool = True

            return {check_bool, seasons}

        # if it has been a month since the last check (max season)
        if self.current_time - last_update > update_interval:
            seasons = pd.Series(self.max_season_id)
            check_bool = True

        return {check_bool, seasons}

    def checkPlayersImport(self):
        players = pd.Series()
        check_bool = False
        last_update = self.table_log_df.lastUpdate(table_name="players_import")

        # if there are players who haven't been checked (all players)
        cursor, db = db_import_login()

        sql = "select a.playerId from player_bios_import as a left join player_import_log as b on a.playerId = " \
              "b.playerId where b.lastDateUpdated is null"
        players_to_check_df = pd.read_sql(sql, db)

        db.commit()
        cursor.close()
        db.close()

        players_to_check = players_to_check_df['playerId']

        if players_to_check.len() > 0:
            check_bool = True
            players = pd.concat([players, players_to_check])

        # if there are games that have been played since the last check (players from those games)
        cursor, db = db_import_login()

        sql = "select b.playerId from games_import as a join roster_spots_import as b on a.gameId = b.gameId where " \
              "a.gameDate between '"
        sql = "{}{}{}{}".format(sql, last_update, "' and '", self.current_time, "'")
        players_to_check_df = pd.read_sql(sql, db)

        db.commit()
        cursor.close()
        db.close()

        if players_to_check_df.len() > 0:
            check_bool = True
            players = pd.concat([players, players_to_check])

        players = players.unique()

        return {check_bool, players}

    @staticmethod
    def updateTeamsImport():
        teams = nhlpd.TeamsImport()
        check = teams.queryNHLupdateDB()

        log_object = ImportTableUpdateLog()
        log_object.updateDB("teams_import", check)

    @staticmethod
    def updateSeasonsImport():
        seasons = nhlpd.SeasonsImport()
        check = seasons.queryNHLupdateDB()

        log_object = ImportTableUpdateLog()
        log_object.updateDB("seasons_import", check)

    @staticmethod
    def updateGamesImport(seasons):
        for season_id in seasons['seasonId'].items():
            season = nhlpd.GamesImport()

            if season_id == 99999999:
                season.queryNHLupdateDB()
            else:
                season.queryNHLupdateDB(season_id=season_id)

        log_object = ImportTableUpdateLog()
        log_object.updateDB("games_import", 1)

    @staticmethod
    def updateGameCentersImport(games):
        for game_id in games['gameId'].items():
            game_center = nhlpd.GameCenterImport(game_id)
            game_center.queryNHLupdateDB()

        log_object = ImportTableUpdateLog()
        log_object.updateDB("game_center_import", 1)

    @staticmethod
    def updateRostersImport(seasons):
        for season_id in seasons['seasonId'].items():
            rosters = nhlpd.RostersImport()

            if season_id == 99999999:
                rosters.queryNHLupdateDB()
            else:
                rosters.queryNHLupdateDB(season_id=season_id)

        log_object = ImportTableUpdateLog()
        log_object.updateDB("rosters_import", 1)

    @staticmethod
    def updatePlayersImport(players):
        for player_id in players['playerId'].items():
            player = nhlpd.PlayersImport(player_id=player_id)

            player.queryNHLupdateDB()

        log_object = ImportTableUpdateLog()
        log_object.updateDB("player_bios_import", 1)
