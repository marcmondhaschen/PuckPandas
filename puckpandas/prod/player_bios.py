import pandas as pd
import puckpandas as pp
from sqlalchemy import text

class PlayerBios:
    def __init__(self):
        self.table_columns = ['playerId','firstName','lastName','birthDate','birthCountry','birthState','birthCity',
                              'shootsCatches','heightInInches','heightInCentimeters','weightInPounds',
                              'weightInKilograms']
        self.player_bios_df = pd.DataFrame()
        self.query_db()
        self.player_bios_df = self.player_bios_df.reindex(columns=self.table_columns)
        self.current_season = pp.TeamSeasonsImport.current_season()

    def update_db(self):
        if self.player_bios_df.size > 0:
            engine = pp.dba_prod_login()
            sql = """insert into puckpandas.player_bios (playerId, firstName, lastName, birthDate, birthCountry, 
            birthState, birthCity, shootsCatches, heightInInches, heightInCentimeters, weightInPounds, 
            weightInKilograms) select playerId, `firstName.default` as firstName, `lastName.default` as lastName, 
            birthDate, birthCountry, `birthStateProvince.default` as birthState, `birthCity.default` as birthCity, 
            shootsCatches, heightInInches, heightInCentimeters, weightInPounds, weightInKilograms from 
            puckpandas_import.player_bios_import"""

            with engine.connect() as conn:
                conn.execute(text(sql))

        return True

    @staticmethod
    def clear_db():
        engine = pp.dba_prod_login()
        sql = "delete from puckpandas.player_bios"

        with engine.connect() as conn:
            conn.execute(text(sql))
        engine.dispose()

        return True

    def query_db(self):
        engine = pp.dba_prod_login()
        sql = "select playerId, firstName, lastName, birthDate, birthCountry, birthState, birthCity, shootsCatches, " \
              "heightInInches, heightInCentimeters, weightInPounds, weightInKilograms from puckpandas.player_bios"
        player_bios_df = pd.read_sql_query(sql, engine)
        engine.dispose()

        if player_bios_df.size > 0:
            player_bios_df = player_bios_df.reindex(columns=self.table_columns)
            player_bios_df.infer_objects().fillna('', inplace=True)
            player_bios_df.drop_duplicates(inplace=True)
            self.player_bios_df = player_bios_df

        return self.player_bios_df
