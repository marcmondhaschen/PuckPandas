from datetime import datetime
import pandas as pd
from .api_query import fetch_json_data
from .mysql_db import db_import_login


class PlayersImport:
    goalie_df = pd.DataFrame(columns=[''])
    skater_df = pd.DataFrame(columns=[''])
    position = ''
    json = {}

    def __init__(self, goalie_df=pd.DataFrame(), skater_df=pd.DataFrame(), position=None, json=None):
        self.goalie_df = pd.concat([self.goalie_df, goalie_df])
        self.skater_df = pd.concat([self.skater_df, skater_df])
        self.position = '' if position is None else self.position = position
        self.json = {} if json is None else self.json = json

    def updateDB(self):
        return True

    @staticmethod
    def clearDB(player_id=''):
        return True

    def queryDB(self, player_id=''):
        return True

    def queryNHL(self, player_id=''):

        return True

    def queryNHLupdateDB(self, player_id=''):
        self.queryNHL(player_id)
        self.clearDB(player_id)
        self.updateDB()

        return True


class PlayerBiosImport:
    _df = pd.DataFrame(columns=[''])
    json = {}

    def __init__():
        self.json = {} if json is None else self.json = json

    def updateDB(self):
        return True

    @staticmethod
    def clearDB(player_id=''):
        return True

    def queryDB(self, player_id=''):
        return True

    def queryNHL(self, player_id=''):
        return True

    def queryNHLupdateDB(self, player_id=''):
        self.queryNHL(player_id)
        self.clearDB(player_id)
        self.updateDB()

        return True


class SkaterCareerTotalsImport:
    _df = pd.DataFrame(columns=[''])
    json = {}

    def __init__():
        self.json = {} if json is None else self.json = json

    def updateDB(self):
        return True

    @staticmethod
    def clearDB(player_id=''):
        return True

    def queryDB(self, player_id=''):
        return True

    def queryNHL(self, player_id=''):
        return True

    def queryNHLupdateDB(self, player_id=''):
        self.queryNHL(player_id)
        self.clearDB(player_id)
        self.updateDB()

        return True


class SkaterSeasonImport:
    _df = pd.DataFrame(columns=[''])
    json = {}

    def __init__():
        self.json = {} if json is None else self.json = json

    def updateDB(self):
        return True

    @staticmethod
    def clearDB(player_id=''):
        return True

    def queryDB(self, player_id=''):
        return True

    def queryNHL(self, player_id=''):
        return True

    def queryNHLupdateDB(self, player_id=''):
        self.queryNHL(player_id)
        self.clearDB(player_id)
        self.updateDB()

        return True


class GoalieCareerTotalsImport:
    career_totals_df = pd.DataFrame(columns=[''])
    json = {}

    def __init__():
        self.json = {} if json is None else self.json = json

    def updateDB(self):
        cursor, db = db_import_login()

        for index, row in self.career_totals_df.iterrows():
            sql = "insert into goalie_career_totals_import (playerId, `regularSeason.gamesPlayed`, " \
                  "`regularSeason.goals`, `regularSeason.assists`, `regularSeason.pim`, `regularSeason.gamesStarted`, " \
                  "`regularSeason.points`, `regularSeason.wins`, `regularSeason.losses`, `regularSeason.otLosses`, " \
                  "`regularSeason.shotsAgainst`, `regularSeason.goalsAgainst`, `regularSeason.goalsAgainstAvg`, " \
                  "`regularSeason.savePctg`, `regularSeason.shutouts`, `regularSeason.timeOnIce`, " \
                  "`regularSeason.timeOnIceMinutes`, `regularSeason.timeOnIceSeconds`, " \
                  "`playoffs.gamesPlayed`, `playoffs.goals`, `playoffs.assists`, `playoffs.pim`, " \
                  "`playoffs.gamesStarted`, `playoffs.points`, `playoffs.wins`, `playoffs.losses`, " \
                  "`playoffs.otLosses`, `playoffs.shotsAgainst`, `playoffs.goalsAgainst`, `playoffs.goalsAgainstAvg`, " \
                  "`playoffs.savePctg`, `playoffs.shutouts`, `playoffs.timeOnIce`, `playoffs.timeOnIceMinutes`, " \
                  "`playoffs.timeOnIceSeconds`) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, " \
                  "%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            val = ([row['playerId'], row['regularSeason.gamesPlayed'], row['regularSeason.goals'],
                    row['regularSeason.assists'], row['regularSeason.pim'], row['regularSeason.gamesStarted'],
                    row['regularSeason.points'], row['regularSeason.wins'], row['regularSeason.losses'],
                    row['regularSeason.otLosses'], row['regularSeason.shotsAgainst'], row['regularSeason.goalsAgainst'],
                    row['regularSeason.goalsAgainstAvg'], row['regularSeason.savePctg'], row['regularSeason.shutouts'],
                    row['regularSeason.timeOnIce'], row['regularSeason.timeOnIceMinutes'],
                    row['regularSeason.timeOnIceSeconds'], row['playoffs.gamesPlayed'], row['playoffs.goals'],
                    row['playoffs.assists'], row['playoffs.pim'], row['playoffs.gamesStarted'], row['playoffs.points'],
                    row['playoffs.wins'], row['playoffs.losses'], row['playoffs.otLosses'], row['playoffs.shotsAgainst'],
                    row['playoffs.goalsAgainst'], row['playoffs.goalsAgainstAvg'], row['playoffs.savePctg'],
                    row['playoffs.shutouts'], row['playoffs.timeOnIce'], row['playoffs.timeOnIceMinutes'],
                    row['playoffs.timeOnIceSeconds']])

            cursor.execute(sql, val)

        db.commit()
        cursor.close()
        db.close()

        return True

    @staticmethod
    def clearDB(player_id=''):
        return True

    def queryDB(self, player_id=''):
        return True

    def queryNHL(self, player_id=''):
        return True

    def queryNHLupdateDB(self, player_id=''):
        self.queryNHL(player_id)
        self.clearDB(player_id)
        self.updateDB()

        return True


class GoalieSeasonImport:
    season_totals_df = pd.DataFrame(columns=[''])
    json = {}

    def __init__():
        self.json = {} if json is None else self.json = json

    def updateDB(self):
        cursor, db = db_import_login()

        for index, row in self.season_totals_df.iterrows():
            sql = "insert into goalie_season_import (playerId, gameTypeId, gamesPlayed, goalsAgainst, " \
                  "goalsAgainstAvg, leagueAbbrev, losses, season, sequence, shutouts, ties, timeOnIce, " \
                  "timeOnIceMinutes, timeOnIceSeconds, wins, `teamName.default`, savePctg, shotsAgainst, otLosses, " \
                  "assists, gamesStarted, goals, pim) values " \
                  "(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            val = ([row['playerId'], row['gameTypeId'], row['gamesPlayed'], row['goalsAgainst'], row['goalsAgainstAvg'],
                    row['leagueAbbrev'], row['losses'], row['season'], row['sequence'], row['shutouts'], row['ties'],
                    row['timeOnIce'], row['timeOnIceMinutes'], row['timeOnIceSeconds'], row['wins'],
                    row['teamName.default'], row['savePctg'], row['shotsAgainst'], row['otLosses'], row['assists'],
                    row['gamesStarted'], row['goals'], row['pim']])

            cursor.execute(sql, val)

        # tidy up the cursors
        db.commit()
        cursor.close()
        db.close()

        return True

    @staticmethod
    def clearDB(player_id=''):
        return True

    def queryDB(self, player_id=''):
        return True

    def queryNHL(self, player_id=''):
        return True

    def queryNHLupdateDB(self, player_id=''):
        self.queryNHL(player_id)
        self.clearDB(player_id)
        self.updateDB()

        return True


class PlayerAwardsImport:
    _df = pd.DataFrame(columns=[''])
    json = {}

    def __init__():
        self.json = {} if json is None else self.json = json

    def updateDB(self):
        return True

    @staticmethod
    def clearDB(player_id=''):
        return True

    def queryDB(self, player_id=''):
        return True

    def queryNHL(self, player_id=''):
        return True

    def queryNHLupdateDB(self, player_id=''):
        self.queryNHL(player_id)
        self.clearDB(player_id)
        self.updateDB()

        return True


def fetch_players():
    """
    Queries the NHL API for a player bio and game stats details

    Parameters:

    Returns: True - returns True upon completion
    """

    if len(player_id_df) == 0:
        return False

    for index, row in player_id_df.iterrows():
        player_id = row['playerId']

        url_prefix = 'https://api-web.nhle.com/v1/player/'
        url_suffix = '/landing'
        url_string = "{}{}{}".format(url_prefix, player_id, url_suffix)
        json_data = fetch_json_data(url_string)

        if json_data != {}:
            # player bio
            player_bio_df = pd.json_normalize(json_data)
            master_bio_df = master_player_frame()
            player_bio_df = pd.concat([master_bio_df, player_bio_df])
            player_bio_df = transform_player_frame(player_bio_df)
            player_bio_check = load_player_frame(player_bio_df)

            position = player_bio_df.at[0, 'position']

            if 'careerTotals' in json_data:
                # career totals
                career_totals_df = pd.json_normalize(json_data, record_path=['careerTotals'], meta=['playerId'])
                career_totals_df = career_totals_df.fillna('')

                if position == 'G':
                    # goalie career totals
                    master_goalie_career_df = master_goalie_career_frame()
                    career_totals_df = pd.concat([master_goalie_career_df, career_totals_df])
                    career_totals_df = transform_goalie_career_frame(career_totals_df)
                    career_check = load_goalie_career_frame(career_totals_df)
                else:
                    # skater career totals
                    master_player_career_df = master_player_career_frame()
                    career_totals_df = pd.concat([master_player_career_df, career_totals_df])
                    career_totals_df = transform_player_career_frame(career_totals_df)
                    career_check = load_player_career_frame(career_totals_df)
            else:
                career_check = False

            if 'seasonTotals' in json_data:
                # season totals
                season_totals_df = pd.json_normalize(json_data, record_path=['seasonTotals'], meta=['playerId'])
                season_totals_df = season_totals_df.fillna('')

                if position == 'G':
                    # goalie season totals
                    master_goalie_season_df = master_goalie_season_frame()
                    season_totals_df = pd.concat([master_goalie_season_df, season_totals_df])
                    season_totals_df = transform_goalie_season_frame(season_totals_df)
                    season_check = load_goalie_season_frame(season_totals_df)
                else:
                    # skater season totals
                    master_player_season_df = master_player_season_frame()
                    season_totals_df = pd.concat([master_player_season_df, season_totals_df])
                    season_totals_df = transform_player_season_frame(season_totals_df)
                    season_check = load_player_season_frame(season_totals_df)
            else:
                season_check = False

            if 'awards' in json_data:
                # awards
                awards_df = pd.json_normalize(json_data['awards'],
                                              record_path=['seasons'],
                                              meta=[['trophy', 'default']])
                awards_df.insert(loc=0, column='playerId', value=player_id)

                master_award_df = master_player_award_frame()
                awards_df = pd.concat([master_award_df, awards_df])
                awards_df = transform_player_award_frame(awards_df)
                awards_check = load_player_award_frame(awards_df)
            else:
                # awards array is absent where player has no NHL awards
                awards_check = False

        else:
            # no records for this playerId
            player_bio_check = career_check = season_check = awards_check = False

        check_date = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
        check_log_df = pd.DataFrame(data=[[player_id, check_date, player_bio_check, career_check, season_check,
                                           awards_check]],
                                    columns=['playerId', 'logDate', 'playerBio', 'career', 'season', 'awards'])
        check_log_df = check_log_df.fillna('')
        update_player_log(check_log_df)

    return True


def master_player_frame():
    """
    Manually builds an empty Pandas Dataframe with columns consistent with player bio information

    Parameters:

    Returns: play_by_play_df - an empty Pandas Dataframe with columns consistent with a player's bio information
    """
    player_bio_df = pd.DataFrame(columns=['playerId', 'isActive', 'currentTeamId', 'currentTeamAbbrev', 'sweaterNumber',
                                          'position', 'heightInInches', 'heightInCentimeters', 'weightInPounds',
                                          'weightInKilograms', 'birthDate', 'birthCountry', 'shootsCatches',
                                          'inTop100AllTime', 'inHHOF', 'firstName.default', 'lastName.default',
                                          'birthCity.default', 'birthStateProvince.default', 'draftDetails.year',
                                          'draftDetails.teamAbbrev', 'draftDetails.round', 'draftDetails.pickInRound',
                                          'draftDetails.overallPick'])
    return player_bio_df


def master_player_award_frame():
    """
    Manually builds an empty Pandas Dataframe with columns consistent with trophy and awards info, by season

    Parameters:

    Returns: player_award_df - an empty Pandas Dataframe with columns consistent with trophy and awards info, by season
    """
    player_award_df = pd.DataFrame(columns=['playerId', 'seasonId', 'trophy.default'])

    return player_award_df


def master_goalie_career_frame():
    """
    Manually builds an empty Pandas Dataframe with columns consistent with goalie career summary statistics

    Parameters:

    Returns: goalie_career_df - an empty Pandas Dataframe with columns consistent with goalie career summary statistics
    """
    goalie_career_df = pd.DataFrame(columns=['playerId', 'regularSeason.gamesPlayed', 'regularSeason.goals',
                                             'regularSeason.assists', 'regularSeason.pim', 'regularSeason.gamesStarted',
                                             'regularSeason.points', 'regularSeason.wins', 'regularSeason.losses',
                                             'regularSeason.otLosses', 'regularSeason.shotsAgainst',
                                             'regularSeason.goalsAgainst', 'regularSeason.goalsAgainstAvg',
                                             'regularSeason.savePctg', 'regularSeason.shutouts',
                                             'regularSeason.timeOnIce', 'regularSeason.timeOnIceMinutes',
                                             'regularSeason.timeOnIceSeconds',
                                             'playoffs.gamesPlayed', 'playoffs.goals',
                                             'playoffs.assists', 'playoffs.pim', 'playoffs.gamesStarted',
                                             'playoffs.points', 'playoffs.wins', 'playoffs.losses', 'playoffs.otLosses',
                                             'playoffs.shotsAgainst', 'playoffs.goalsAgainst',
                                             'playoffs.goalsAgainstAvg', 'playoffs.savePctg',
                                             'playoffs.shutouts', 'playoffs.timeOnIce',
                                             'playoffs.timeOnIceMinutes', 'playoffs.timeOnIceSeconds'])
    return goalie_career_df


def master_goalie_season_frame():
    """
    Manually builds an empty Pandas Dataframe with columns consistent with goalie season summary statistics

    Parameters:

    Returns: goalie_season_df - an empty Pandas Dataframe with columns consistent with goalie season summary statistics
    """
    goalie_season_df = pd.DataFrame(columns=['playerId', 'assists', 'gameTypeId', 'gamesPlayed', 'gamesStarted',
                                             'goals', 'goalsAgainst', 'goalsAgainstAvg', 'leagueAbbrev', 'losses',
                                             'pim', 'season', 'sequence', 'shutouts', 'ties', 'timeOnIce',
                                             'timeOnIceMinutes', 'timeOnIceSeconds', 'wins', 'teamName.default',
                                             'savePctg', 'shotsAgainst', 'otLosses', 'assists', 'gamesStarted',
                                             'goals', 'pim'])
    return goalie_season_df


def master_player_career_frame():
    """
    Manually builds an empty Pandas Dataframe with columns consistent with player career summary statistics

    Parameters:

    Returns: player_career_df - an empty Pandas Dataframe with columns consistent with player career summary statistics
    """
    player_career_df = pd.DataFrame(columns=['playerId', 'regularSeason.gamesPlayed', 'regularSeason.goals',
                                             'regularSeason.assists', 'regularSeason.pim',
                                             'regularSeason.points', 'regularSeason.plusMinus',
                                             'regularSeason.powerPlayGoals', 'regularSeason.powerPlayPoints',
                                             'regularSeason.shorthandedPoints', 'regularSeason.gameWinningGoals',
                                             'regularSeason.otGoals', 'regularSeason.shots',
                                             'regularSeason.shootingPctg', 'regularSeason.faceoffWinningPctg',
                                             'regularSeason.avgToi', 'regularSeason.shorthandedGoals',
                                             'playoffs.gamesPlayed', 'playoffs.goals', 'playoffs.assists',
                                             'playoffs.pim', 'playoffs.points', 'playoffs.plusMinus',
                                             'playoffs.powerPlayGoals', 'playoffs.powerPlayPoints',
                                             'playoffs.shorthandedPoints', 'playoffs.gameWinningGoals',
                                             'playoffs.otGoals', 'playoffs.shots',
                                             'playoffs.shootingPctg', 'playoffs.faceoffWinningPctg',
                                             'playoffs.avgToi', 'playoffs.shorthandedGoals'])

    return player_career_df


def master_player_season_frame():
    """
    Manually builds an empty Pandas Dataframe with columns consistent with player season summary statistics

    Parameters:

    Returns: player_season_df - an empty Pandas Dataframe with columns consistent with player season summary statistics
    """
    player_season_df = pd.DataFrame(columns=['playerId', 'assists', 'gameTypeId', 'gamesPlayed', 'goals',
                                             'leagueAbbrev', 'pim', 'points', 'season', 'sequence', 'teamName.default',
                                             'gameWinningGoals', 'plusMinus', 'powerPlayGoals', 'shorthandedGoals',
                                             'shots', 'avgToi', 'faceoffWinningPctg', 'otGoals', 'powerPlayPoints',
                                             'shootingPctg', 'shorthandedPoints'])

    return player_season_df


def transform_player_frame(player_bio_df):
    player_bio_df = player_bio_df.fillna('')
    return player_bio_df


def transform_player_award_frame(player_award_df):
    player_award_df = player_award_df.fillna('')
    return player_award_df


def transform_goalie_career_frame(career_totals_df):
    career_totals_df = career_totals_df.fillna(0)
    # Pandas has a hard time with large-minute time values, and MySQL can't store times of more than 839 hours
    # we'll need to convert some columns' time values to integer seconds before storing them
    if career_totals_df.loc[0, 'regularSeason.timeOnIce'] != 0:
        career_totals_df[['regularSeason.timeOnIceMinutes', 'regularSeason.timeOnIceSeconds']] = \
            career_totals_df['regularSeason.timeOnIce'].str.split(":", expand=True)
        career_totals_df['regularSeason.timeOnIceSeconds'] = \
            int(career_totals_df['regularSeason.timeOnIceMinutes'].iloc[0])*60 + \
            int(career_totals_df['regularSeason.timeOnIceSeconds'].iloc[0])
    if career_totals_df.loc[0, 'playoffs.timeOnIce'] != 0:
        career_totals_df[['playoffs.timeOnIceMinutes', 'playoffs.timeOnIceSeconds']] = \
            career_totals_df['playoffs.timeOnIce'].str.split(":", expand=True)
        career_totals_df['playoffs.timeOnIceSeconds'] = \
            int(career_totals_df['playoffs.timeOnIceMinutes'].iloc[0])*60 + \
            int(career_totals_df['playoffs.timeOnIceSeconds'].iloc[0])
    return career_totals_df


def transform_goalie_season_frame(season_totals_df):
    if not season_totals_df.empty:
        season_totals_df = season_totals_df.fillna(0)
        season_totals_df.loc[season_totals_df.timeOnIce == '', 'timeOnIce'] = '0:00'
        season_totals_df.loc[season_totals_df.timeOnIce == 0, 'timeOnIce'] = '0:00'
        season_totals_df[['timeOnIceMinutes', 'timeOnIceSeconds']] = \
            season_totals_df['timeOnIce'].str.split(":", expand=True)
        season_totals_df['timeOnIceSeconds'] = \
            season_totals_df['timeOnIceMinutes'].astype(int)*60 + season_totals_df['timeOnIceSeconds'].astype(int)
    return season_totals_df


def transform_player_career_frame(career_totals_df):
    career_totals_df = career_totals_df.fillna('')
    return career_totals_df


def transform_player_season_frame(season_totals_df):
    season_totals_df = season_totals_df.fillna('')
    return season_totals_df


def load_player_frame(player_bio_df):
    """
    Inserts player biography into the local SQL database

    Parameters: player_bio_df - a DataFrame object containing player biography info

    Returns: True - returns True upon completion
    """


    return True



def load_player_career_frame(career_totals_df):
    """
    Inserts player career summary statistics into the local database

    Parameters: career_totals_df - a Dataframe object containing player summarized career statistics

    Returns: True - returns True upon completion
    """
    cursor, db = db_import_login()

    for index, row in career_totals_df.iterrows():
        sql = "insert into skater_career_totals_import (playerId, `regularSeason.gamesPlayed`, " \
              "`regularSeason.goals`, `regularSeason.assists`, `regularSeason.pim`, `regularSeason.points`, " \
              "`regularSeason.plusMinus`, `regularSeason.powerPlayGoals`, `regularSeason.powerPlayPoints`, " \
              "`regularSeason.shorthandedPoints`, `regularSeason.gameWinningGoals`, `regularSeason.otGoals`, " \
              "`regularSeason.shots`, `regularSeason.shootingPctg`, `regularSeason.faceoffWinningPctg`, " \
              "`regularSeason.avgToi`, `regularSeason.shorthandedGoals`, `playoffs.gamesPlayed`, `playoffs.goals`, " \
              "`playoffs.assists`, `playoffs.pim`, `playoffs.points`, `playoffs.plusMinus`, " \
              "`playoffs.powerPlayGoals`, `playoffs.powerPlayPoints`, `playoffs.shorthandedPoints`, " \
              "`playoffs.gameWinningGoals`, `playoffs.otGoals`, `playoffs.shots`, `playoffs.shootingPctg`, " \
              "`playoffs.faceoffWinningPctg`, `playoffs.avgToi`, `playoffs.shorthandedGoals`) values (%s, %s, %s, " \
              "%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, " \
              "%s, %s, %s, %s, %s)"
        val = ([row['playerId'], row['regularSeason.gamesPlayed'], row['regularSeason.goals'],
                row['regularSeason.assists'], row['regularSeason.pim'], row['regularSeason.points'],
                row['regularSeason.plusMinus'], row['regularSeason.powerPlayGoals'],
                row['regularSeason.powerPlayPoints'], row['regularSeason.shorthandedPoints'],
                row['regularSeason.gameWinningGoals'], row['regularSeason.otGoals'], row['regularSeason.shots'],
                row['regularSeason.shootingPctg'], row['regularSeason.faceoffWinningPctg'], row['regularSeason.avgToi'],
                row['regularSeason.shorthandedGoals'], row['playoffs.gamesPlayed'], row['playoffs.goals'],
                row['playoffs.assists'], row['playoffs.pim'], row['playoffs.points'], row['playoffs.plusMinus'],
                row['playoffs.powerPlayGoals'], row['playoffs.powerPlayPoints'], row['playoffs.shorthandedPoints'],
                row['playoffs.gameWinningGoals'], row['playoffs.otGoals'], row['playoffs.shots'],
                row['playoffs.shootingPctg'], row['playoffs.gameWinningGoals'], row['playoffs.avgToi'],
                row['playoffs.shorthandedGoals']])

        cursor.execute(sql, val)

    # tidy up the cursors
    db.commit()
    cursor.close()
    db.close()

    return True


# TODO - add error checking on return
def load_player_season_frame(season_totals_df):
    """
    Inserts player statistics summarized by season into the local database

    Parameters: season_totals_df - a DataFrame containing player stats totals by season

    Returns: True - returns True upon completion
    """
    cursor, db = db_import_login()

    for index, row in season_totals_df.iterrows():
        sql = "insert into skater_season_import (playerId, assists, gameTypeId, gamesPlayed, goals, " \
              "leagueAbbrev, pim, points, season, sequence, `teamName.default`, gameWinningGoals, plusMinus, " \
              "powerPlayGoals, shorthandedGoals, shots, faceoffWinningPctg, avgToi, otGoals, powerPlayPoints, " \
              "shootingPctg, shorthandedPoints) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, " \
              "%s, %s, %s, %s, %s, %s, %s)"
        val = ([row['playerId'], row['assists'], row['gameTypeId'], row['gamesPlayed'], row['goals'],
                row['leagueAbbrev'], row['pim'], row['points'], row['season'], row['sequence'], row['teamName.default'],
                row['gameWinningGoals'], row['plusMinus'], row['powerPlayGoals'], row['shorthandedGoals'], row['shots'],
                row['faceoffWinningPctg'], row['avgToi'], row['otGoals'], row['powerPlayPoints'], row['shootingPctg'],
                row['shorthandedPoints']])

        cursor.execute(sql, val)

    # tidy up the cursors
    db.commit()
    cursor.close()
    db.close()

    return True


# TODO - add error checking on return
def load_player_award_frame(awards_df):
    """
    Inserts trophy & award records into the player_award_import table

    Parameters: awards_df - a DataFrame with trophies awarded to a given player by seasonId

    Returns: True - returns True upon completion
    """
    cursor, db = db_import_login()

    for index, row in awards_df.iterrows():
        sql = 'insert into player_award_import (playerId, seasonId, `trophy.default`) values (%s, %s, %s)'
        val = [row['playerId'], row['seasonId'], row['trophy.default']]
    
        cursor.execute(sql, val)

    # tidy up the cursors
    db.commit()
    cursor.close()
    db.close()

    return True
