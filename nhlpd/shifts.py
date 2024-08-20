from datetime import datetime
import pandas as pd
from .api_query import fetch_json_data
from .mysql_db import db_import_login


def fetch_shifts_to_query():
    """
    Queries the local SQL database for a list of games to have their shifts queried from the NHL

    Parameters: none

    Returns: game_id_df - a Pandas Dataframe containing gameIds
    """
    games_sql = "select a.gameId from games_import as a left join shift_import_log as b " \
                "on a.gameId = b.gameId where b.gameId is null;"

    cursor, db = db_import_login()
    game_id_df = pd.read_sql(games_sql, db)

    return game_id_df


def fetch_shifts():
    """
    Queries the NHL API for shift details by player for each game

    Parameters: none

    Returns:
    """

    game_id_df = fetch_shifts_to_query()

    if len(game_id_df) == 0:
        return False

    for index, row in game_id_df.iterrows():
        game_id = row['gameId']
        shifts_load_check = False

        url_prefix = 'https://api.nhle.com/stats/rest/en/shiftcharts?cayenneExp=gameId='
        url_string = "{}{}".format(url_prefix, game_id)
        json_data = fetch_json_data(url_string)

        if len(json_data['data']) > 0:
            shifts_df = pd.json_normalize(json_data, record_path=['data'])
            master_shifts_df = master_shift_frame()
            shifts_df = pd.concat([shifts_df, master_shifts_df])
            shifts_df = transform_shifts_frame(shifts_df)
            shifts_load_check = load_shifts_frame(shifts_df)

        log_date = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
        log_df = pd.DataFrame(data=[[game_id, log_date, shifts_load_check]],
                              columns=['gameId', 'logDate', 'checked'])
        log_df = log_df.fillna('')
        update_shift_log(log_df)

    return True


def master_shift_frame():
    """ Manually builds an empty Pandas Dataframe with columns consistent with shift statistics

    Parameters: none

    Returns: shifts_df - an empty Pandas Dataframe with columns consistent with shift statistics
    """
    shifts_df = pd.DataFrame(columns=['id', 'detailCode', 'duration', 'endTime', 'eventDescription', 'eventDetails',
                                      'firstName', 'gameId', 'hexValue', 'lastName', 'period', 'playerId',
                                      'shiftNumber', 'startTime', 'teamAbbrev', 'teamId', 'teamName', 'typeCode'])

    return shifts_df


def transform_shifts_frame(shifts_df):
    """
    Transforms shifts import data so that it's ready to import into the database

    Parameters: shifts_df - a Dataframe that requires transformation before it's ready to be loaded to the database

    Returns: shifts_df - a Dataframe object that is ready to be loaded into the database
    """
    shifts_df = shifts_df.fillna('')
    return shifts_df


def load_shifts_frame(shifts_df):
    """
    Inserts shift records into the shifts_import table

    Parameters: shifts_df - a DataFrame with shifts played for each player and gameId

    Returns: True - returns True upon completion
    """
    cursor, db = db_import_login()

    for index, row in shifts_df.iterrows():
        sql = 'insert into shifts_import (id, detailCode, duration, endTime, eventDescription, eventDetails, ' \
              'eventNumber, firstName, gameId, hexValue, lastName, period, playerId, shiftNumber, startTime, ' \
              'teamAbbrev, teamId, teamName, typeCode) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, ' \
              '%s, %s, %s, %s, %s, %s, %s)'
        val = [row['id'], row['detailCode'], row['duration'], row['endTime'], row['eventDescription'],
               row['eventDetails'], row['eventNumber'], row['firstName'], row['gameId'], row['hexValue'],
               row['lastName'], row['period'], row['playerId'], row['shiftNumber'], row['startTime'], row['teamAbbrev'],
               row['teamId'], row['teamName'], row['typeCode']]

        cursor.execute(sql, val)

    # tidy up the cursors
    db.commit()
    cursor.close()
    db.close()

    return True


def update_shift_log(log_df):
    """
    Logs when each game's shifts are recorded.

    Parameters: log_df - a DataFrame with a set of gameIds and their boolean checked/unchecked status

    Returns: True - returns True upon completion
    """
    cursor, db = db_import_login()

    for index, row in log_df.iterrows():
        sql = "insert into shift_import_log (gameId, logDate, checked) values (%s, %s, %s)"
        val = [row['gameId'], row['logDate'], row['checked']]

        cursor.execute(sql, val)

    # tidy up the cursors
    db.commit()
    cursor.close()
    db.close()

    return True


def etl_shifts():
    """
    Queries the local database for a list of games with no shift data, queries that data from the NHL, and loads it
    to the local database

    Parameters: none

    Returns: checkvar - a bool to verify that function has run
    """
    check_var = fetch_shifts()
    return check_var
