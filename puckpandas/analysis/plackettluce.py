import pandas as pd
from sqlalchemy import text
import puckpandas as pp


class PowerRankDates:
    def __init__(self):
        self.table_columns = ['seasonId', 'endDate', 'gameDateRank', '7DayStartDate', '7DayStartRank',
                              '14DayStartDate', '14DayStartRank', '21DayStartDate', '21DayStartRank', '28DayStartDate',
                              '28DayStartRank', '1DaySampleDate', '1DaySampleRank', '2DaySampleEndDate',
                              '2DaySampleEndRank', '7DaySampleEndDate', '7DaySampleEndRank']
        self.dates_df = pd.DataFrame()
        self.query_db()
        self.dates_df = self.dates_df.reindex(columns=self.table_columns)

    def update_db(self):
        if self.dates_df.size > 0:
            engine = pp.db_ana_login()
            sql = "insert into puckpandas_ana.ana_power_rank_dates_base select a.seasonId, a.gameDate, rank() " \
                  "over (partition by a.seasonId order by a.gameDate) as gameDateRank, a.gameCount) from " \
                  "(select g.seasonId, g.gameDate, count(g.gameId) as gameCount from puckpandas.games as g where " \
                  "gameType = 2 and seasonId >= 20002001 and seasonId not in (20122013, 20192020,20202021) group by " \
                  "g.seasonId, g.gameDate) as a"
            sql2 = "insert into puckpandas_ana.ana_power_rank_date_spreads select a.seasonId, a.gameDate as " \
                   "endDate, a.gameDateRank, coalesce(b.gameDate,'') as 7DayStartDate, coalesce(b.gameDateRank,'') " \
                   "as 7DayStartRank, coalesce(c.gameDate,'') as 14DayStartDate, coalesce(c.gameDateRank,'') as " \
                   "14DayStartRank, coalesce(d.gameDate,'') as 21DayStartDate, coalesce(d.gameDateRank,'') as " \
                   "21DayStartRank, coalesce(e.gameDate,'') as 28DayStartDate, coalesce(e.gameDateRank,'') as " \
                   "28DayStartRank, coalesce(f.gameDate,'') as 1DaySampleDate, coalesce(f.gameDateRank,'') " \
                   "1DaySampleRank, coalesce(g.gameDate,'') as 2DaySampleEndDate, coalesce(g.gameDateRank,'') " \
                   "2DaySampleEndRank, coalesce(h.gameDate,'') as 7DaySampleEndDate, coalesce(h.gameDateRank,'') " \
                   "7DaySampleEndRank from puckpandas_ana.ana_power_rank_dates_base as a left join " \
                   "puckpandas_ana.ana_power_rank_dates_base as b on a.seasonId = b.seasonId and a.gameDateRank = " \
                   "b.gameDateRank + 6 left join puckpandas_ana.ana_power_rank_dates_base as c on a.seasonId = " \
                   "c.seasonId and a.gameDateRank = c.gameDateRank + 13 left join " \
                   "puckpandas_ana.ana_power_rank_dates_base as d on a.seasonId = d.seasonId and a.gameDateRank = " \
                   "d.gameDateRank + 20 left join puckpandas_ana.ana_power_rank_dates_base as e on a.seasonId = " \
                   "e.seasonId and a.gameDateRank = e.gameDateRank + 27 left join " \
                   "puckpandas_ana.ana_power_rank_dates_base as f on a.seasonId = f.seasonId and a.gameDateRank + 1 " \
                   "= f.gameDateRank left join puckpandas_ana.ana_power_rank_dates_base as g on a.seasonId = " \
                   "g.seasonId and a.gameDateRank + 2 = g.gameDateRank left join " \
                   "puckpandas_ana.ana_power_rank_dates_base as h on a.seasonId = h.seasonId and a.gameDateRank + " \
                   "7 = h.gameDateRank"

            with engine.connect() as conn:
                conn.execute(text(sql))
                conn.execute(text(sql2))

        return True

    @staticmethod
    def clear_db():
        engine = pp.db_ana_login()
        sql = "delete from puckpandas_ana.ana_power_rank_dates_base"
        sql2 = "delete from puckpandas_ana.ana_power_rank_date_spreads"
        with engine.connect() as conn:
            conn.execute(text(sql))
            conn.execute(text(sql2))
            engine.dispose()

        return True

    def query_db(self):
        engine = pp.db_ana_login()
        sql = "select seasonId, endDate, gameDateRank, 7DayStartDate, 7DayStartRank, 14DayStartDate, 14DayStartRank, " \
              "21DayStartDate, 21DayStartRank, 28DayStartDate, 28DayStartRank, 1DaySampleDate, 1DaySampleRank, " \
              "2DaySampleEndDate, 2DaySampleEndRank, 7DaySampleEndDate, 7DaySampleEndRank from " \
              "puckpandas_ana.ana_power_rank_date_spreads"
        dates_df = pd.read_sql_query(sql, engine)
        engine.dispose()

        if dates_df.size > 0:
            dates_df = dates_df.reindex(columns=self.table_columns)
            dates_df.infer_objects().fillna('', inplace=True)
            self.dates_df = dates_df

        return self.dates_df


class PowerRankIterator:
    # iterates over the ana_power_rank_dates table
    def __init__(self):
        self.power_rank_dates = PowerRankDates()
        self.games_object = pp.Games()
            # should build and use a games object for games prod
            # said object needs to be able to call games by date range
        self.games_results_object = pp.GameResults()
            # should build and use a games results object for games_results prod
        self.games_data_frame = pd.DataFrame() # will contain row of gameIDs


    @staticmethod
    def iterateOverDatesThinger():

        pass

    @staticmethod
    def pollDatabaseForGames(start_date, stop_date):
        pass

    @staticmethod
    def pollDatabaseForTeams():
        pass

    @staticmethod
    def formatDatabaseGamesForChoix():
        pass


class PowerRankTest:
    # tests a single power ranking against a list of games
    # records results to database table
    pass


class PowerRankTestIterator:
    # iterates a single power ranking over a list of tests (row from table ana_power_rank_date_spreads)
    # usage should immediately follow calc of a set of daily power ranks
    pass
