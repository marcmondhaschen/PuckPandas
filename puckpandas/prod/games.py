import pandas as pd
import puckpandas as pp
from sqlalchemy import text


class Games:
    def __init__(self):
        self.table_columns = ['gameId', 'seasonId', 'gameType', 'gameDate', 'venueId', 'startTimeUTC',
                              'startTimeVenue', 'awayTeam', 'homeTeam']
        self.games_df = pd.DataFrame()
        self.query_db()
        self.games_df = self.games_df.reindex(columns=self.table_columns)

    def update_db(self, season_id=0):
        if self.games_df.size > 0:
            engine = pp.dba_prod_login()

            if season_id != 0:
                sql = """insert into puckpandas.games (gameId, seasonId, gameType, gameDate, venueId, startTimeUTC, 
                startTimeVenue, awayTeam, homeTeam) select a.gameId, a.seasonId, a.gameType, a.gameDate, b.venueId, 
                a.startTimeUTC, date_add(a.startTimeUTC, INTERVAL time_to_sec(left(a.venueUTCOffset, locate(':', 
                a.venueUTCOffset)+2)) second) as startTimeVenue, a.awayTeam, a.homeTeam from 
                puckpandas_import.games_import as a join puckpandas.venues as b on a.venue = b.venue where 
                a.seasonId = """ + str(season_id)
            else:
                sql = """insert into puckpandas.games (gameId, seasonId, gameType, gameDate, venueId, startTimeUTC, 
                startTimeVenue, awayTeam, homeTeam) select a.gameId, a.seasonId, a.gameType, a.gameDate, b.venueId, 
                a.startTimeUTC, date_add(a.startTimeUTC, INTERVAL time_to_sec(left(a.venueUTCOffset, locate(':', 
                a.venueUTCOffset)+2)) second) as startTimeVenue, a.awayTeam, a.homeTeam from 
                puckpandas_import.games_import as a join puckpandas.venues as b on a.venue = b.venue"""

            with engine.connect() as conn:
                conn.execute(text(sql))

        return True

    @staticmethod
    def clear_db(season_id=0):
        engine = pp.dba_prod_login()
        sql = """delete from puckpandas.games"""

        if season_id != 0:
            sql += """ where seasonId = """ + str(season_id)

        with engine.connect() as conn:
            conn.execute(text(sql))
        engine.dispose()

        return True

    def query_db(self):
        engine = pp.dba_prod_login()
        sql = """select gameId, seasonId, gameType, gameDate, venueId, startTimeUTC, startTimeVenue, awayTeam, 
        homeTeam from puckpandas.games"""

        games_df = pd.read_sql_query(sql, engine)
        engine.dispose()

        if games_df.size > 0:
            games_df = games_df.reindex(columns=self.table_columns)
            games_df.infer_objects().fillna('', inplace=True)
            games_df.drop_duplicates(inplace=True)
            self.games_df = games_df

        return self.games_df
