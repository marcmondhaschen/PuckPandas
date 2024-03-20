from datetime import datetime
import pandas as pd
from api_query import fetch_json_data
from mysql_db import nhlpandas_db_login

# TODO document functions on this page
# TODO query here is kinda smelly. Reconsider underlying data structures. Maybe combine them or query after we've
#  moved the supporting tables out of their 'import' state?


def nhl_pandas_fetch_players_to_query():
    """
    Queries the local SQL database for a list of players to be queried from the NHL

    Parameters:

    Returns: player_id_df - a Pandas Dataframe containing playerIds
    """
    players_sql = "select distinct a.playerId from (select playerId from game_rosters_import union select playerId " \
                  "from rosters_import) as a where a.playerId not in (select playerId from player_import_log) order " \
                  "by playerId"

    cursor, db = nhlpandas_db_login()
    player_id_df = pd.read_sql(players_sql, db)

    return player_id_df


# TODO - add error check on return
def nhl_pandas_fetch_players():
    """
    Queries the NHL API for player details

    Parameters:

    Returns: True - returns True upon completion
    """
    player_id_df = nhl_pandas_fetch_players_to_query()

    if len(player_id_df) == 0:
        return False

    for index, row in player_id_df.iterrows():
        player_id = row['playerId']

        url_prefix = 'https://api-web.nhle.com/v1/player/'
        url_suffix = '/landing'
        url_string = "{}{}{}".format(url_prefix, player_id, url_suffix)
        json_data = fetch_json_data(url_string)

        if json_data != {}:
            player_bio_df = pd.json_normalize(json_data)
            position = player_bio_df.at[0, 'position']
            master_bio_df = nhlpandas_master_player_frame()
            player_bio_df = pd.concat([master_bio_df, player_bio_df])
            player_bio_df = player_bio_df.fillna('')
            player_bio_check = nhlpandas_load_player_frame(player_bio_df)

            if "careerTotals" in json_data:
                json_career_totals = json_data['careerTotals']
                career_totals_df = pd.json_normalize(json_career_totals)
                career_totals_df.insert(loc=0, column='playerId', value=player_id)
                career_totals_df = career_totals_df.fillna('')

                # goalies have their own set of stats tables
                if position == "G":
                    master_goalie_career_df = nhlpandas_master_goalie_career_frame()
                    career_totals_df = pd.concat([master_goalie_career_df, career_totals_df])
                    career_totals_df = career_totals_df.fillna('')
                    career_check = nhlpandas_load_goalie_career_frame(career_totals_df)
                else:
                    master_player_career_df = nhlpandas_master_player_career_frame()
                    career_totals_df = pd.concat([master_player_career_df, career_totals_df])
                    career_totals_df = career_totals_df.fillna('')
                    career_check = nhlpandas_load_player_career_frame(career_totals_df)
            else:
                career_check = True

            if "seasonTotals" in json_data:
                json_season_totals = json_data['seasonTotals']
                season_totals_df = pd.json_normalize(json_season_totals)
                season_totals_df.insert(loc=0, column='playerId', value=player_id)

                # goalies have their own set of stats tables
                if position == "G":
                    master_goalie_season_df = nhlpandas_master_goalie_season_frame()
                    season_totals_df = pd.concat([master_goalie_season_df, season_totals_df])
                    season_totals_df = season_totals_df.fillna('')
                    season_check = nhlpandas_load_goalie_season_frame(season_totals_df)
                else:
                    master_player_season_df = nhlpandas_master_player_season_frame()
                    season_totals_df = pd.concat([master_player_season_df, season_totals_df])
                    season_totals_df = season_totals_df.fillna('')
                    season_check = nhlpandas_load_player_season_frame(season_totals_df)
            else:
                season_check = True

            if "awards" in json_data:
                awards_df = pd.json_normalize(json_data['awards'],
                                              record_path=['seasons'],
                                              meta=[['trophy', 'default']])
                awards_df.insert(loc=0, column='playerId', value=player_id)

                master_award_df = nhlpandas_master_player_award_frame()
                awards_df = pd.concat([master_award_df, awards_df])
                awards_df = awards_df.fillna('')
                awards_check = nhlpandas_load_player_award_frame(awards_df)
            # awards array is absent where player has no NHL awards
            else:
                awards_check = True

        else:
            player_bio_check = career_check = season_check = awards_check = True

        check_date = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
        check_log_df = pd.DataFrame(data=[[player_id, check_date, player_bio_check, career_check, season_check,
                                           awards_check]],
                                    columns=['playerId', 'logDate', 'playerBio', 'career', 'season', 'awards'])
        check_log_df = check_log_df.fillna('')
        nhlpandas_update_player_log(check_log_df)

    return True


def nhlpandas_master_player_frame():
    player_bio_df = pd.DataFrame(columns=['playerId', 'isActive', 'currentTeamId', 'currentTeamAbbrev', 'sweaterNumber',
                                          'position', 'heightInInches', 'heightInCentimeters', 'weightInPounds',
                                          'weightInKilograms', 'birthDate', 'birthCountry', 'shootsCatches',
                                          'inTop100AllTime', 'inHHOF', 'firstName.default', 'lastName.default',
                                          'birthCity.default', 'birthStateProvince.default', 'draftDetails.year',
                                          'draftDetails.teamAbbrev', 'draftDetails.round', 'draftDetails.pickInRound',
                                          'draftDetails.overallPick'])
    return player_bio_df


def nhlpandas_master_player_award_frame():
    player_award_df = pd.DataFrame(columns=['playerId', 'seasonId', 'trophy.default'])

    return player_award_df


def nhlpandas_master_goalie_career_frame():
    goalie_career_df = pd.DataFrame(columns=['playerId', 'regularSeason.gamesPlayed', 'regularSeason.goals',
                                             'regularSeason.assists', 'regularSeason.pim', 'regularSeason.gamesStarted',
                                             'regularSeason.points', 'regularSeason.wins', 'regularSeason.losses',
                                             'regularSeason.otLosses', 'regularSeason.shotsAgainst',
                                             'regularSeason.goalsAgainst', 'regularSeason.goalsAgainstAvg',
                                             'regularSeason.savePctg', 'regularSeason.shutouts',
                                             'regularSeason.timeOnIce', 'playoffs.gamesPlayed', 'playoffs.goals',
                                             'playoffs.assists', 'playoffs.pim', 'playoffs.gamesStarted',
                                             'playoffs.points', 'playoffs.wins', 'playoffs.losses', 'playoffs.otLosses',
                                             'playoffs.shotsAgainst', 'playoffs.goalsAgainst',
                                             'playoffs.goalsAgainstAvg', 'playoffs.savePctg',
                                             'playoffs.shutouts', 'playoffs.timeOnIce'])
    return goalie_career_df


def nhlpandas_master_goalie_season_frame():
    goalie_season_df = pd.DataFrame(columns=['playerId', 'gameTypeId', 'gamesPlayed', 'goalsAgainst', 'goalsAgainstAvg',
                                             'leagueAbbrev', 'losses', 'season', 'sequence', 'shutouts', 'ties',
                                             'timeOnIce', 'wins', 'teamName.default', 'savePctg', 'shotsAgainst',
                                             'otLosses', 'assists', 'gamesStarted', 'goals', 'pim'])
    return goalie_season_df


def nhlpandas_master_player_career_frame():
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


def nhlpandas_master_player_season_frame():
    player_season_df = pd.DataFrame(columns=['playerId', 'assists', 'gameTypeId', 'gamesPlayed', 'goals',
                                             'leagueAbbrev', 'pim', 'points', 'season', 'sequence', 'teamName.default',
                                             'gameWinningGoals', 'plusMinus', 'powerPlayGoals', 'shorthandedGoals',
                                             'shots', 'avgToi', 'faceoffWinningPctg', 'otGoals', 'powerPlayPoints',
                                             'shootingPctg', 'shorthandedPoints'])

    return player_season_df


def nhlpandas_load_player_frame(player_bio_df):
    cursor, db = nhlpandas_db_login()

    for index, row in player_bio_df.iterrows():
        sql = "insert into player_bios_import (playerId, isActive, currentTeamId, currentTeamAbbrev, " \
              "sweaterNumber, position, heightInInches, heightInCentimeters, weightInPounds, " \
              "weightInKilograms, birthDate, birthCountry, shootsCatches, inTop100AllTime, inHHOF, " \
              "`firstName.default`, `lastName.default`, `birthCity.default`, `birthStateProvince.default`, " \
              "`draftDetails.year`, `draftDetails.teamAbbrev`, `draftDetails.round`, `draftDetails.pickInRound`, " \
              "`draftDetails.overallPick`) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, " \
              "%s, %s, %s, %s, %s, %s, %s, %s)"
        val = (row['playerId'], row['isActive'], row['currentTeamId'],
               row['currentTeamAbbrev'], row['sweaterNumber'], row['position'],
               row['heightInInches'], row['heightInCentimeters'], row['weightInPounds'],
               row['weightInKilograms'], row['birthDate'], row['birthCountry'],
               row['shootsCatches'], row['inTop100AllTime'], row['inHHOF'],
               row['firstName.default'], row['lastName.default'],
               row['birthCity.default'], row['birthStateProvince.default'],
               row['draftDetails.year'], row['draftDetails.teamAbbrev'],
               row['draftDetails.round'], row['draftDetails.pickInRound'],
               row['draftDetails.overallPick'])
        cursor.execute(sql, val)

    # tidy up the cursors
    db.commit()
    cursor.close()
    db.close()

    return True


def nhlpandas_load_goalie_career_frame(career_totals_df):
    cursor, db = nhlpandas_db_login()

    for index, row in career_totals_df.iterrows():
        sql = "insert into goalie_career_totals_import (playerId, `regularSeason.gamesPlayed`, `regularSeason.goals`," \
              "`regularSeason.assists`, `regularSeason.pim`, `regularSeason.gamesStarted`, `regularSeason.points`, " \
              "`regularSeason.wins`, `regularSeason.losses`, `regularSeason.otLosses`, `regularSeason.shotsAgainst`, " \
              "`regularSeason.goalsAgainst`, `regularSeason.goalsAgainstAvg`, `regularSeason.savePctg`, " \
              "`regularSeason.shutouts`, `regularSeason.timeOnIce`, `playoffs.gamesPlayed`, `playoffs.goals`, " \
              "`playoffs.assists`, `playoffs.pim`, `playoffs.gamesStarted`, `playoffs.points`, `playoffs.wins`, " \
              "`playoffs.losses`, `playoffs.otLosses`, `playoffs.shotsAgainst`, `playoffs.goalsAgainst`, " \
              "`playoffs.goalsAgainstAvg`, `playoffs.savePctg`, `playoffs.shutouts`, `playoffs.timeOnIce`) values " \
              "(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, " \
              "%s, %s, %s, %s, %s, %s)"
        val = ([row['playerId'], row['regularSeason.gamesPlayed'], row['regularSeason.goals'],
                row['regularSeason.assists'], row['regularSeason.pim'], row['regularSeason.gamesStarted'],
                row['regularSeason.points'], row['regularSeason.wins'], row['regularSeason.losses'],
                row['regularSeason.otLosses'], row['regularSeason.shotsAgainst'], row['regularSeason.goalsAgainst'],
                row['regularSeason.goalsAgainstAvg'], row['regularSeason.savePctg'], row['regularSeason.shutouts'],
                row['regularSeason.timeOnIce'], row['playoffs.gamesPlayed'], row['playoffs.goals'],
                row['playoffs.assists'], row['playoffs.pim'], row['playoffs.gamesStarted'], row['playoffs.points'],
                row['playoffs.wins'], row['playoffs.losses'], row['playoffs.otLosses'], row['playoffs.shotsAgainst'],
                row['playoffs.goalsAgainst'], row['playoffs.goalsAgainstAvg'], row['playoffs.savePctg'],
                row['playoffs.shutouts'], row['playoffs.timeOnIce']])
    
        cursor.execute(sql, val)

    # tidy up the cursors
    db.commit()
    cursor.close()
    db.close()

    return True


def nhlpandas_load_goalie_season_frame(season_totals_df):
    cursor, db = nhlpandas_db_login()

    for index, row in season_totals_df.iterrows():
        sql = "insert into goalie_season_import (playerId, gameTypeId, gamesPlayed, goalsAgainst, goalsAgainstAvg, " \
              "leagueAbbrev, losses, season, sequence, shutouts, ties, timeOnIce, wins, `teamName.default`, " \
              "savePctg, shotsAgainst, otLosses, assists, gamesStarted, goals, pim) values (%s, %s, %s, %s, %s, %s, " \
              "%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        val = ([row['playerId'], row['gameTypeId'], row['gamesPlayed'], row['goalsAgainst'], row['goalsAgainstAvg'],
                row['leagueAbbrev'], row['losses'], row['season'], row['sequence'], row['shutouts'], row['ties'],
                row['timeOnIce'], row['wins'], row['teamName.default'], row['savePctg'], row['shotsAgainst'],
                row['otLosses'], row['assists'], row['gamesStarted'], row['goals'], row['pim']])

        cursor.execute(sql, val)

    # tidy up the cursors
    db.commit()
    cursor.close()
    db.close()

    return True


def nhlpandas_load_player_career_frame(career_totals_df):
    cursor, db = nhlpandas_db_login()

    for index, row in career_totals_df.iterrows():
        sql = "insert into player_career_totals_import (playerId, `regularSeason.gamesPlayed`, " \
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


def nhlpandas_load_player_season_frame(season_totals_df):
    cursor, db = nhlpandas_db_login()

    for index, row in season_totals_df.iterrows():
        sql = "insert into player_season_import (playerId, assists, gameTypeId, gamesPlayed, goals, leagueAbbrev, " \
              "pim, points, season, sequence, `teamName.default`, gameWinningGoals, plusMinus, powerPlayGoals, " \
              "shots, faceoffWinningPctg, avgToi, otGoals, powerPlayPoints, shootingPctg, shorthandedPoints) values (" \
              "%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        val = ([row['playerId'], row['assists'], row['gameTypeId'], row['gamesPlayed'], row['goals'],
                row['leagueAbbrev'], row['pim'], row['points'], row['season'], row['sequence'], row['teamName.default'],
                row['gameWinningGoals'], row['plusMinus'], row['powerPlayGoals'], row['shots'],
                row['faceoffWinningPctg'], row['avgToi'], row['otGoals'], row['powerPlayPoints'], row['shootingPctg'],
                row['shorthandedPoints']])

        cursor.execute(sql, val)

    # tidy up the cursors
    db.commit()
    cursor.close()
    db.close()

    return True


def nhlpandas_load_player_award_frame(awards_df):
    cursor, db = nhlpandas_db_login()

    for index, row in awards_df.iterrows():
        sql = 'insert into player_award_import (playerId, seasonId, `trophy.default`) values (%s, %s, %s)'
        val = [row['playerId'], row['seasonId'], row['trophy.default']]
    
        cursor.execute(sql, val)

    # tidy up the cursors
    db.commit()
    cursor.close()
    db.close()

    return True


def nhlpandas_update_player_log(check_log_df):
    cursor, db = nhlpandas_db_login()

    for index, row in check_log_df.iterrows():
        sql = "insert into player_import_log (playerId, logDate, playerBio, career, season, awards) values (%s, %s, " \
              "%s, %s, %s, %s)"
        val = [row['playerId'], row['logDate'], row['playerBio'], row['career'], row['season'], row['awards']]

        cursor.execute(sql, val)

    # tidy up the cursors
    db.commit()
    cursor.close()
    db.close()

    return True


def nhlpandas_etl_players():
    check_var = nhl_pandas_fetch_players()
    return check_var
