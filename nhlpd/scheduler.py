from datetime import datetime, timezone
import numpy as np
import pandas as pd
import nhlpd


class Scheduler:
    def __init__(self):
        self.current_time = np.datetime64(datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S"))
        self.current_month = pd.Timestamp(self.current_time).month
        self.current_year = pd.Timestamp(self.current_time).year
        self.max_season_id = self.set_max_season()

        self.table_log = nhlpd.ImportTableUpdateLog()

    @staticmethod
    def set_max_season():
        engine = nhlpd.dba_import_login()
        sql = "select max(seasonId) as seasonId from team_seasons_import"
        max_df = pd.read_sql_query(sql, engine)
        engine.dispose()

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
        max_season_start_year = int(self.max_season_id[0:4])
        max_season_end_year = int(self.max_season_id[4:8])

        # if there's no record in the log
        if last_update is None:
            check_bool = True

            return check_bool

        # if we are in a play season & our database has the current season we pass, otherwise run
        if self.current_month >= 9 and self.current_year == max_season_start_year:
            check_bool = False
        elif self.current_month < 6 and self.current_year == max_season_end_year:
            check_bool = False
        else:
            check_bool = True

        return check_bool

    def check_games_import(self):
        check_bool = False
        last_update = self.table_log.last_update(table_name="games_import")

        # if there's no record in the log (all seasons)
        if last_update is None:
            data = {'seasonId': ['99999999']}
            seasons = pd.DataFrame.from_dict(data)
            check_bool = True
            return {"check_bool": check_bool, "seasons": seasons}

        # if there's a new season (new seasons)
        seasons = nhlpd.SeasonsImportLog.seasons_without_games()
        if seasons.size > 0:
            check_bool = True
            return {"check_bool": check_bool, "seasons": seasons}

        # if games this season have been played since the last_update (current season)
        games = nhlpd.GamesImportLog.games_between_dates(last_update, self.current_time)
        if games.size > 0:
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

    def check_game_centers_import(self):
        check_bool = False
        last_update = self.table_log.last_update(table_name="game_center_import")
        import_log = nhlpd.GamesImportLog()
        last_minus_two_weeks = ''
        if last_update != '':
            last_minus_two_weeks = last_update - np.timedelta64(14, 'D')

        # if there are unchecked games in the games_import_log table
        unpolled_games = import_log.games_not_queried()

        # if there are recently played games, since the last update
        recent_games = import_log.games_played_recently(last_minus_two_weeks, self.current_time)

        games = pd.concat([unpolled_games, recent_games])

        if games.size > 0:
            check_bool = True

        return {"check_bool": check_bool, "games": games}

    def check_shifts_import(self):
        # shift records don't start until 20102011 season
        check_bool = False
        last_update = self.table_log.last_update(table_name="game_center_import")
        import_log = nhlpd.GamesImportLog()
        last_minus_two_weeks = ''
        if last_update != '':
            last_minus_two_weeks = last_update - np.timedelta64(14, 'D')

        # if there are games where we haven't checked for shift data
        unpolled_games = import_log.shifts_not_queried()

        # if there are games played recently with no shift data
        recent_games = import_log.games_played_recently(last_minus_two_weeks, self.current_time)

        games = pd.concat([unpolled_games, recent_games])

        if games.size > 0:
            check_bool = True

        return {"check_bool": check_bool, "games": games}

    def check_rosters_import(self):
        update_interval = np.timedelta64(30, 'D')
        check_bool = False
        last_update = self.table_log.last_update(table_name="rosters_import")

        # if there's no record in the log (all seasons)
        if last_update is None:
            data = {'seasonId': ['99999999']}
            seasons = pd.DataFrame.from_dict(data)
            check_bool = True

            return {"check_bool": check_bool, "seasons": seasons}

        # if there are seasons we haven't logged rosters from (new seasons)
        seasons = nhlpd.SeasonsImportLog.seasons_without_rosters()

        if seasons.size > 0:
            check_bool = True

            return {"check_bool": check_bool, "seasons": seasons}

        # if it has been a month since the last check (max season)
        if self.current_time - last_update > update_interval:
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

    def check_players_import(self):
        check_bool = False
        last_update = self.table_log.last_update(table_name="player_bios_import")
        import_log = nhlpd.PlayerImportLog()
        last_minus_two_weeks = ''
        if last_update != '':
            last_minus_two_weeks = last_update - np.timedelta64(14, 'D')

        # update the player_import_log table for any new players
        import_log.insert_untracked_players()

        # if there are players who haven't been checked (all players)
        unpolled_players = import_log.players_not_queried()

        # if there are games that have been played since the last check (players from those games)
        recently_played = import_log.players_played_recently(last_minus_two_weeks, self.current_time)

        players = pd.concat([unpolled_players, recently_played])

        if players.size > 0:
            check_bool = True

        return {"check_bool": check_bool, "players": players}

    def update_teams_import(self):
        teams = nhlpd.TeamsImport()
        teams.query_nhl_update_db()

        log_object = nhlpd.ImportTableUpdateLog()
        log_object.update_db("teams_import", 1)
        self.table_log = nhlpd.ImportTableUpdateLog()

        return True

    def update_seasons_import(self):
        seasons = nhlpd.SeasonsImport()
        seasons.query_nhl_update_db()

        log_object = nhlpd.ImportTableUpdateLog()
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

        log_object = nhlpd.ImportTableUpdateLog()
        log_object.update_db("games_import", 1)
        self.table_log = nhlpd.ImportTableUpdateLog()

        return True

    def update_game_centers_import(self, games):
        for index, row in games.iterrows():
            game_center = nhlpd.GameCenterImport(row['gameId'])
            game_center.query_nhl_update_db()

        log_object = nhlpd.ImportTableUpdateLog()
        log_object.update_db("game_center_import", 1)
        self.table_log = nhlpd.ImportTableUpdateLog()

        return True

    def update_shifts_import(self, games):
        for index, row in games.iterrows():
            shifts = nhlpd.ShiftsImport(row['gameId'])
            shifts.query_nhl_update_db()

        log_object = nhlpd.ImportTableUpdateLog()
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
            team_season = nhlpd.RostersImport(team_id=row['teamId'], season_id=row['seasonId'])
            team_season.query_nhl_update_db()

        log_object = nhlpd.ImportTableUpdateLog()
        log_object.update_db("rosters_import", 1)
        self.table_log = nhlpd.ImportTableUpdateLog()

        return True

    def update_players_import(self, players):
        for idx, player_id in players['playerId'].items():
            player = nhlpd.PlayersImport(player_id=player_id)
            player.query_nhl_update_db()

        log_object = nhlpd.ImportTableUpdateLog()
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

        roster_check = self.check_rosters_import()
        if roster_check['check_bool'] and len(roster_check['seasons']) > 0:
            self.update_rosters_import(roster_check['seasons'])

        player_check = self.check_players_import()
        if player_check['check_bool'] and player_check['players'].size > 0:
            self.update_players_import(player_check['players'])

        return True
