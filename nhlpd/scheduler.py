from datetime import datetime, timezone
import pandas as pd
import nhlpd
from .mysql_db import db_import_login
from .import_table_update_log import ImportTableUpdateLog
import numpy as np


class Scheduler:
    def __init__(self):
        self.current_time = np.datetime64(datetime.now(timezone.utc))
        self.current_month = pd.Timestamp(self.current_time).month
        self.current_year = pd.Timestamp(self.current_time).year
        self.max_season_id = self.set_max_season()

        self.table_log = nhlpd.ImportTableUpdateLog()

        self.game_log_df = self.query_db_for_games()
        self.player_log_df = self.query_db_for_players()

    @staticmethod
    def query_db_for_games():
        cursor, db = db_import_login()

        sql = "select a.gameId, a.lastDateUpdated, a.gameFound, a.gameCenterFound, a.tvBroadcastsFound, " \
              "a.playsFound, a.rosterSpotsFound, a.teamGameStatsFound, a.seasonSeriesFound, a.refereesFound, " \
              "a.linesmenFound, a.scratchesFound, a.shiftsFound from games_import_log as a join (select gameId, " \
              "max(lastDateUpdated) as lastDateUpdated from games_import_log group by gameId) as b on a.gameId = " \
              "b.gameId and a.lastDateUpdated = b.lastDateUpdated"
        game_log_df = pd.read_sql(sql, db)

        db.commit()
        cursor.close()
        db.close()

        return game_log_df

    @staticmethod
    def query_db_for_players():
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
    def set_max_season():
        cursor, db = db_import_login()
        sql = "select max(seasonId) as seasonId from team_seasons_import"
        max_df = pd.read_sql(sql, db)

        db.commit()
        cursor.close()
        db.close()

        max_season_id = max_df.at[0, 'seasonId']

        if max_season_id is None:
            max_season_id = ''

        return max_season_id

    def check_teams_import(self):
        update_interval = np.timedelta64(180, 'D')
        check_bool = False
        last_update = self.table_log.last_update(table_name="teams_import")

        # if there's no record in the log
        if last_update is None:
            check_bool = True

            return check_bool

        # if it's been six months since the last check
        if self.current_time - last_update > update_interval:
            check_bool = True

        return check_bool

    def check_seasons_import(self):
        last_update = self.table_log.last_update(table_name="team_seasons_import")

        # if there's no record in the log
        if last_update is None:
            check_bool = True

            return check_bool

        max_season_start_year = int(self.max_season_id[0:4])
        max_season_end_year = int(self.max_season_id[4:8])

        # if we are in a play season & our database has the current season we pass, otherwise run
        if self.current_month >= 9 and self.current_year == max_season_start_year:
            check_bool = False
        elif self.current_month < 6 and self.current_year == max_season_end_year:
            check_bool = False
        else:
            check_bool = True

        return check_bool

    def check_games_import(self):
        seasons = pd.DataFrame()
        check_bool = False
        last_update = self.table_log.last_update(table_name="games_import")

        # if there's no record in the log (all seasons)
        if last_update is None:
            data = {'seasonId': ['99999999']}
            seasons = pd.DataFrame.from_dict(data)
            check_bool = True

            return {"check_bool": check_bool, "seasons": seasons}

        # if there's a new season (new seasons)
        cursor, db = db_import_login()
        new_season_sql = "select a.seasonId, count(b.gameId) as gameCount from team_seasons_import as a left join " \
                         "games_import as b on a.seasonId = b.seasonId group by a.seasonId having gameCount = 0"
        new_seasons_df = pd.read_sql(new_season_sql, db)

        db.commit()
        cursor.close()
        db.close()

        if new_seasons_df.size > 0:
            data = new_seasons_df['seasonId']
            seasons = pd.DataFrame.from_dict(data)
            check_bool = True

            return {"check_bool": check_bool, "seasons": seasons}

        # if games this season have been played since the last_update (current season)
        cursor, db = db_import_login()
        fresh_games_sql_prefix = "select gameId from games_import where gameDate between '"
        fresh_games_sql_suffix = "' and '"
        fresh_games_sql = "{}{}{}{}'".format(fresh_games_sql_prefix, last_update, fresh_games_sql_suffix,
                                             str(self.current_time))
        games_since_update = pd.read_sql(fresh_games_sql, db)

        db.commit()
        cursor.close()
        db.close()

        if games_since_update.size > 0:
            data = {'seasonId': [self.max_season_id]}
            seasons = pd.DataFrame.from_dict(data)
            check_bool = True

            return {"check_bool": check_bool, "seasons": seasons}

        # if we're in this season's playoffs (current season)
        if 4 <= self.current_month <= 6:
            data = {'seasonId': [self.max_season_id]}
            seasons = pd.DataFrame.from_dict(data)
            check_bool = True

        return {"check_bool": check_bool, "seasons": seasons}

    @staticmethod
    def check_game_centers_import():
        games = pd.DataFrame()
        check_bool = False

        # if there are unchecked games in the games_import_log table
        cursor, db = db_import_login()
        sql = "select gameId from games_import_log where gameFound = 1 and gameCenterFound = 0"
        games_to_check_df = pd.read_sql(sql, db)
        db.commit()
        cursor.close()
        db.close()

        if games_to_check_df.size > 0:
            games = games_to_check_df
            check_bool = True

        return {"check_bool": check_bool, "games": games}

    @staticmethod
    def check_shifts_import():
        # shift records don't start until 20102011 season
        games = pd.DataFrame()
        check_bool = False

        # if there are unchecked games in the games_import_log table
        cursor, db = db_import_login()
        sql = "select a.gameId from games_import_log as a join games_import as b on a.gameId = b.gameId where " \
              "a.gameFound = 1 and a.shiftsFound = 0 and b.seasonId >= 20102011"
        games_to_check_df = pd.read_sql(sql, db)
        db.commit()
        cursor.close()
        db.close()

        if games_to_check_df.size > 0:
            games = games_to_check_df
            check_bool = True

        return {"check_bool": check_bool, "games": games}

    def check_rosters_import(self):
        update_interval = np.timedelta64(30, 'D')
        seasons = pd.DataFrame()
        check_bool = False
        last_update = self.table_log.last_update(table_name="rosters_import")

        # if there's no record in the log (all seasons)
        if last_update is None:
            data = {'seasonId': [99999999]}
            seasons = pd.DataFrame.from_dict(data)
            check_bool = True

            return {"check_bool": check_bool, "seasons": seasons}

        # if there's a new season in the DB (new seasons)
        cursor, db = db_import_login()
        sql = "select a.seasonId, count(b.playerId) as playerCount from team_seasons_import as a left join " \
              "rosters_import as b on a.seasonId = b.seasonId group by a.seasonId having playerCount = 0"
        new_seasons_df = pd.read_sql(sql, db)

        db.commit()
        cursor.close()
        db.close()

        if seasons.len() > 0:
            seasons = pd.concat([seasons, pd.Series([new_seasons_df['seasonId']], name='season_id')])
            check_bool = True

            return {"check_bool": check_bool, "seasons": seasons}

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
            seasons = pd.concat([seasons, pd.Series([self.max_season_id], name='season_id')])
            check_bool = True

            return {"check_bool": check_bool, "seasons": seasons}

        # if it has been a month since the last check (max season)
        if self.current_time - last_update > update_interval:
            seasons = pd.concat([seasons, pd.Series([self.max_season_id], name='season_id')])
            check_bool = True

        return {"check_bool": check_bool, "seasons": seasons}

    def check_players_import(self):
        players = pd.Series()
        check_bool = False
        last_update = self.table_log.last_update(table_name="players_import")

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

        return {"check_bool": check_bool, "players": players}

    def update_teams_import(self):
        teams = nhlpd.TeamsImport()
        teams.query_nh_lupdate_db()

        log_object = ImportTableUpdateLog()
        log_object.update_db("teams_import", 1)
        self.table_log = nhlpd.ImportTableUpdateLog()

        return True

    def update_seasons_import(self):
        seasons = nhlpd.SeasonsImport()
        seasons.query_nhl_update_db()

        log_object = ImportTableUpdateLog()
        log_object.update_db("team_seasons_import", 1)
        self.table_log = nhlpd.ImportTableUpdateLog()

        return True

    def update_games_import(self, seasons):
        update_seasons = nhlpd.SeasonsImport().seasons_df
        update_seasons.sort_values(by=['seasonId', 'teamId'], inplace=True)

        if seasons['seasonId'].values[0] != '99999999':
            bool_mask = update_seasons['seasonId'].isin(seasons['seasonId'])
            update_seasons = update_seasons[bool_mask]

        for index, row in update_seasons.iterrows():
            team_season = nhlpd.GamesImport(team_id=row['teamId'], season_id=row['seasonId'])
            team_season.query_nhl_update_db()

        log_object = ImportTableUpdateLog()
        log_object.update_db("games_import", 1)
        self.table_log = nhlpd.ImportTableUpdateLog()

        return True

    def update_game_centers_import(self, games):
        for index, row in games.iterrows():
            game_center = nhlpd.GameCenterImport(row['gameId'])
            game_center.query_nhl_update_db()

        log_object = ImportTableUpdateLog()
        log_object.update_db("game_center_import", 1)
        self.table_log = nhlpd.ImportTableUpdateLog()

        return True

    def update_shifts_import(self, games):
        for index, row in games.iterrows():
            shifts = nhlpd.ShiftsImport(row['gameId'])
            shifts.query_nhl_update_db()

        log_object = ImportTableUpdateLog()
        log_object.update_db("shifts_import", 1)
        self.table_log = nhlpd.ImportTableUpdateLog()

        return True

    def update_rosters_import(self, seasons):
        update_seasons = nhlpd.SeasonsImport().seasons_df
        update_seasons.sort_values(by=['seasonId', 'teamId'], inplace=True)

        if seasons['seasonId'].values[0] != '99999999':
            bool_mask = update_seasons['seasonId'].isin(seasons['seasonId'])
            update_seasons = update_seasons[bool_mask]

        for index, row in update_seasons.iterrows():
            team_roster = nhlpd.GamesImport(team_id=row['teamId'], season_id=row['seasonId'])
            team_roster.query_nhl_update_db()

        log_object = ImportTableUpdateLog()
        log_object.update_db("rosters_import", 1)
        self.table_log = nhlpd.ImportTableUpdateLog()

        return True

    def update_players_import(self, players):
        for player_id in players['playerId'].items():
            player = nhlpd.PlayersImport(player_id=player_id)
            player.query_nhl_update_db()

        log_object = ImportTableUpdateLog()
        log_object.update_db("player_bios_import", 1)
        self.table_log = nhlpd.ImportTableUpdateLog()

        return True

    def poll_nhl(self):
        if self.check_teams_import():
            self.update_teams_import()

        if self.check_seasons_import():
            self.update_seasons_import()

        game_check = self.check_games_import()
        if game_check['check_bool'] and len(game_check['seasons']) > 0:
            self.update_games_import(game_check['seasons'])

        game_center_check = self.check_game_centers_import()
        if game_center_check['check_bool'] and len(game_center_check['games']) > 0:
            self.update_game_centers_import(game_center_check['games'])

        shifts_check = self.check_shifts_import()
        if shifts_check['check_bool'] and shifts_check['games'].size > 0:
            self.update_shifts_import(shifts_check['games'])

        return True
