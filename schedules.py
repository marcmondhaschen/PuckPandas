import pandas as pd
from api_query import fetch_json_data
from mysql_db import nhlpandas_db_login


# TODO write a function to update the `games` table for games that were scheduled into the future at the last polling,
#  but have since happened
def nhlpandas_fetch_schedules():
    """
    Queries the local MySQL database for a list of seasons played for each team and uses that list to query the NHL API
    for a list of games played for each

    Parameters:

    Returns: schedules_df - a Pandas Dataframe object containing schedules, by game, for each NHL team and season
    provided
    """
    # query all the seasons played from the local db

    team_schedules_sql = 'select triCode, seasonId from team_seasons_import'

    cursor, db = nhlpandas_db_login()
    team_schedules_df = pd.read_sql(team_schedules_sql, db)

    # query schedules played for each team and season from NHL
    schedules_df = pd.DataFrame()

    for index, row in team_schedules_df.iterrows():
        base_url = 'https://api-web.nhle.com/v1/club-schedule-season/'
        query_string = "{}{}/{}".format(base_url, row['triCode'], row['seasonId'])
        json_data = fetch_json_data(query_string)

        team_schedule_df = pd.json_normalize(json_data['games'])

        schedules_df = pd.concat([schedules_df, team_schedule_df])

    # tidy up the cursors
    db.commit()
    cursor.close()
    db.close()

    return schedules_df


# format the seasons dataframe
def nhlpandas_transform_schedules(schedules_df):
    """
    Transforms the Pandas dataframe to ready it for import into the local MySQL database

    Parameters: schedules_df - the Pandas Dataframe object to be transformed

    Returns: schedules_df - the transformed Pandas Dataframe object
    """
    # we're pulling the schedule from each teams' schedule, so we need to remove duplicates
    schedules_df = schedules_df.astype(str).drop_duplicates()
    # Change nan values to null for MySQL
    schedules_df = schedules_df.fillna('')
    return schedules_df


# TODO error checking on return
def nhlpandas_load_seasons_schedules(schedules_df):
    """
    Imports the transformed schedules DataFrame into the local MySQL database

    Parameters: schedules_df - a Pandas Dataframe object containing schedules, by game, for each NHL team and season

    Returns: True - Returns True upon completion
    """
    cursor, db = nhlpandas_db_login()

    for index, row in schedules_df.iterrows():
        sql = "insert into games_import (gameId, seasonId, gameType, gameDate, venue, neutralSite, startTimeUTC, " \
              "venueUTCOffset, venueTimezone, gameState, gameScheduleState, awayTeam, awayTeamSplitSquad, " \
              "awayTeamScore, homeTeam, homeTeamSplitSquad, homeTeamScore, periodType, gameOutcome) values " \
              "(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        val = (row['id'], row['season'], row['gameType'], row['gameDate'], row['venue.default'], row['neutralSite'],
               row['startTimeUTC'], row['venueUTCOffset'], row['venueTimezone'], row['gameState'],
               row['gameScheduleState'], row['awayTeam.id'], row['awayTeam.awaySplitSquad'],
               row['awayTeam.score'], row['homeTeam.id'], row['homeTeam.homeSplitSquad'], row['homeTeam.score'],
               row['periodDescriptor.periodType'], row['gameOutcome.lastPeriodType'])
        cursor.execute(sql, val)

    # tidy up the cursors
    db.commit()
    cursor.close()
    db.close()

    return True


# TODO error checking on return
def nhlpandas_etl_schedules():
    """
    Queries a list of games played for each team and season from the NHL API, transforms the NHL's JSON response into
    a Pandas Dataframe, and imports that DataFrame into a local MySQL table

    Parameters:

    Returns: True - Returns True upon completion
    """
    df = nhlpandas_fetch_schedules()
    df = nhlpandas_transform_schedules(df)
    nhlpandas_load_seasons_schedules(df)

    return True
