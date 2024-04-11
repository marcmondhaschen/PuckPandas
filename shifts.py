from datetime import datetime
import pandas as pd
from api_query import fetch_json_data
from mysql_db import nhlpandas_db_login


def nhl_pandas_fetch_shifts_to_query():
    """
    Queries the local SQL database for a list of games to have their shifts queried from the NHL

    Parameters:

    Returns: game_id_df - a Pandas Dataframe containing gameIds
    """
    games_sql = "select gameId from games_import where gameType in (2, 3) and seasonId >= 20102011"

    cursor, db = nhlpandas_db_login()
    game_id_df = pd.read_sql(games_sql, db)

    return game_id_df
