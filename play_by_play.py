import pandas as pd
from api_query import fetch_json_data
from mysql_db import nhlpandas_db_login


def nhl_pandas_fetch_gameids_to_query():
    """
    Queries the local MySQL database for a list of gameIds for games that have happened (using this moment's date less
    two days) but haven't had their play by play details polled

    Parameters:

    Returns: gameids_df - a Pandas DataFrame object containing a list of gameIds as described above
    """
    gameids_sql = 'select distinct gameId from games_import where gameDate < date_sub(sysdate(), INTERVAL 2 DAY) ' \
                  'and (PBPCheckSuccess is null or PBPCheckSuccess = 0) order by gameDate desc, gameId'
    cursor, db = nhlpandas_db_login()
    gameids_df = pd.read_sql(gameids_sql, db)

    return gameids_df


# TODO add error checking on return
def nhlpandas_fetch_game_details(gameids_df):
    """
    Queries the NHL API for play-by-play and game roster details for each gameId provided

    Parameters: gameids_df - a Pandas Dataframe containing a list of gameIds

    Returns: True - returns True upon completion
    """
    if len(gameids_df) == 0:
        return False

    pbp_master_df = nhlpandas_master_pbp_frame()
    gr_master_df = nhlpandas_master_gr_frame()

    for index, row in gameids_df.iterrows():
        url_prefix = 'https://api-web.nhle.com/v1/gamecenter/'
        url_suffix = '/play-by-play'
        query_url = "{}{}{}".format(url_prefix, row['gameId'], url_suffix)

        json_data = fetch_json_data(query_url)

        if 'plays' in json_data:
            play_by_play_df = pd.json_normalize(json_data, record_path=['plays'], meta=['id'])
            pbp_master_df = pd.concat([pbp_master_df, play_by_play_df])
            pbp_master_df = nhlpandas_transform_play_by_play(pbp_master_df)

        if 'rosterSpots' in json_data:
            game_roster_df = pd.json_normalize(json_data, record_path=['rosterSpots'], meta=['id'])
            gr_master_df = pd.concat([gr_master_df, game_roster_df])
            gr_master_df = nhlpandas_transform_game_rosters(gr_master_df)

        if nhlpandas_load_pbp_details(pbp_master_df):
            pbp_master_df = pbp_master_df.head(0)
        if nhlpandas_load_roster_details(gr_master_df):
            gr_master_df = gr_master_df.head(0)
        nhlpandas_update_gameid_query_log(row['gameId'])

    return True


# TODO add error checking on return
def nhlpandas_update_gameid_query_log(gameid):
    """
    Updates the `games` table to note that the game details (play by play and game rosters) have successfully queried
    and imported

    Parameters: gameId - the specific NHL gameId to be updated

    Returns: True - returns True upon completion
    """
    cursor, db = nhlpandas_db_login()

    sql = "update games_import set PBPCheckSuccess = True, datePBPChecked = CURRENT_DATE where gameId = %s"
    var = [int(gameid)]
    cursor.execute(sql, var)

    return True


def nhlpandas_transform_play_by_play(pbp_df):
    """
    Transforms the Pandas dataframe to ready it for import into the local MySQL database

    Parameters: pbp_df - the Pandas Dataframe object to be transformed

    Returns: pbp_df - the transformed Pandas Dataframe object
    """
    pbp_df = pbp_df.fillna('')
    pbp_df = pbp_df.reset_index(drop=True)
    return pbp_df


def nhlpandas_transform_game_rosters(gr_df):
    """
    Transforms the Pandas dataframe to ready it for import into the local MySQL database

    Parameters: gr_df - the Pandas Dataframe object to be transformed

    Returns: gr_df - the transformed Pandas Dataframe object
    """
    gr_df = gr_df.fillna('')
    gr_df = gr_df.reset_index(drop=True)
    return gr_df


# TODO add error checking on return
def nhlpandas_load_pbp_details(pbp_df):
    """
    Inserts a single game's play-by-play details to the `game_play_by_play` table

    Parameters: pbp_df - a Pandas DataFrame object containing the game's play-by-play events, and details about each
    event

    Returns: True - returns True upon completion
    """

    cursor, db = nhlpandas_db_login()

    for index, row in pbp_df.iterrows():
        sql = "insert into game_play_by_play_import (gameId, eventId, period, periodType, timeInPeriod, " \
              "timeRemaining, situationCode, typeCode, typeDescKey, sortOrder, eventOwnerTeamId, losingPlayerId,  " \
              "winningPlayerId, xCoord, yCoord, zoneCode, reason, hittingPlayerId, hitteePlayerId, shotType, " \
              "shootingPlayerId, goalieInNetId, awaySOG, homeSOG, playerId, blockingPlayerId, secondaryReason, " \
              "detailTypeCode, detailDescKey, detailDuration, detailCommittedByPlayerId, detailDrawnByPlayerId, " \
              "scoringPlayerId, scoringPlayerTotal, assist1PlayerId, assist1PlayerTotal, assist2PlayerId, " \
              "assist2PlayerTotal, awayScore, homeScore) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, " \
              "%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, " \
              "%s, %s)"
        val = (row['id'], row['eventId'], row['periodDescriptor.number'], row['periodDescriptor.periodType'],
               row['timeInPeriod'], row['timeRemaining'], row['situationCode'], row['typeCode'], row['typeDescKey'],
               row['sortOrder'], row['details.eventOwnerTeamId'], row['details.losingPlayerId'],
               row['details.winningPlayerId'], row['details.xCoord'], row['details.yCoord'], row['details.zoneCode'],
               row['details.reason'], row['details.hittingPlayerId'], row['details.hitteePlayerId'],
               row['details.shotType'], row['details.shootingPlayerId'], row['details.goalieInNetId'],
               row['details.awaySOG'], row['details.homeSOG'], row['details.playerId'], row['details.blockingPlayerId'],
               row['details.secondaryReason'], row['details.typeCode'], row['details.descKey'],
               row['details.duration'], row['details.committedByPlayerId'], row['details.drawnByPlayerId'],
               row['details.scoringPlayerId'], row['details.scoringPlayerTotal'], row['details.assist1PlayerId'],
               row['details.assist1PlayerTotal'], row['details.assist2PlayerId'], row['details.assist2PlayerTotal'],
               row['details.awayScore'], row['details.homeScore'])
        cursor.execute(sql, val)

    # tidy up the cursors
    db.commit()
    cursor.close()
    db.close()

    return True


# TODO add error checking on return
def nhlpandas_load_roster_details(gr_df):
    """
    Inserts a single game's roster details to the `game_rosters` table

    Parameters: gr_df - a Pandas DataFrame object containing the game's rosters

    Returns: True - returns True upon completion
    """
    cursor, db = nhlpandas_db_login()

    for index, row in gr_df.iterrows():
        sql = "insert into game_rosters_import (gameId, teamId, playerId, sweaterNumber, positionCode, " \
              "`firstName.default`,`lastName.default`) values (%s, %s, %s, %s, %s, %s, %s)"
        val = (row['id'], row['teamId'], row['playerId'], row['sweaterNumber'], row['positionCode'],
               row['firstName.default'], row['lastName.default'])
        cursor.execute(sql, val)

    # tidy up the cursors
    db.commit()
    cursor.close()
    db.close()

    return True


def nhlpandas_master_pbp_frame():
    """
    Manually builds an empty Pandas Dataframe with columns consistent with a modern game's play-by-play

    Parameters:

    Returns: play_by_play_df - an empty Pandas Dataframe with columns consistent with a modern game's play-by-play
    """

    play_by_play_df = pd.DataFrame(columns=['eventId', 'timeInPeriod', 'timeRemaining', 'situationCode',
                                            'homeTeamDefendingSide', 'typeCode', 'typeDescKey', 'sortOrder',
                                            'periodDescriptor.number', 'periodDescriptor.periodType',
                                            'details.eventOwnerTeamId', 'details.losingPlayerId',
                                            'details.winningPlayerId', 'details.xCoord', 'details.yCoord',
                                            'details.zoneCode', 'details.shotType', 'details.shootingPlayerId',
                                            'details.goalieInNetId', 'details.awaySOG', 'details.homeSOG',
                                            'details.reason', 'details.playerId', 'details.hittingPlayerId',
                                            'details.hitteePlayerId', 'details.scoringPlayerId',
                                            'details.scoringPlayerTotal', 'details.assist1PlayerId',
                                            'details.assist1PlayerTotal', 'details.assist2PlayerId',
                                            'details.assist2PlayerTotal', 'details.awayScore', 'details.homeScore',
                                            'details.blockingPlayerId', 'details.secondaryReason', 'details.typeCode',
                                            'details.descKey', 'details.duration', 'details.committedByPlayerId',
                                            'details.drawnByPlayerId', 'id'])

    return play_by_play_df


def nhlpandas_master_gr_frame():
    """
    Manually builds an empty Pandas Dataframe with columns consistent with a modern game's team rosters

    Parameters:

    Returns: game_roster_df - an empty Pandas Dataframe with columns consistent with a modern game's rosters
    """
    game_roster_df = pd.DataFrame(columns=['teamId', 'playerId', 'sweaterNumber', 'positionCode',
                                           'headshot', 'firstName.default', 'lastName.default', 'id'])

    return game_roster_df


# TODO add error checking on return
def nhlpandas_etl_game_details():
    """
    Queries a list of gameIds from the local SQL database, uses that list to query play-by-play and game details
    from the NHL, formats those details to be loaded to the `game_play_by_play` and `game_rosters tables`, and imports
    to each respective table

    Parameters:

    Returns: checkvar - returns True upon completion
    """
    gameids_df = nhl_pandas_fetch_gameids_to_query()
    check_var = nhlpandas_fetch_game_details(gameids_df)

    return check_var
