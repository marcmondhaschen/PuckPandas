# from datetime import datetime
import nhlpd

# for now, main serves as a program script to test functions
if __name__ == "__main__":
    skater_current = nhlpd.PlayersImport(player_id=8484144)
    skater_retired = nhlpd.PlayersImport(player_id=8470151)
    goalie_current = nhlpd.PlayersImport(player_id=8477967)
    goalie_retired = nhlpd.PlayersImport(player_id=8448382)

    # Connor Bedard
    skater_current.queryNHLupdateDB()
    # Jay Bouwmeester
    skater_retired.queryNHLupdateDB()
    # Thatcher Demko
    goalie_current.queryNHLupdateDB()
    # Curtis Joseph
    goalie_retired.queryNHLupdateDB()

    skater_query_test = nhlpd.PlayersImport(player_id=8484144)
