# from datetime import datetime
import nhlpd

# for now, main serves as a program script to test functions
if __name__ == "__main__":
    skater_current = nhlpd.PlayersImport()
    skater_retired = nhlpd.PlayersImport()
    goalie_current = nhlpd.PlayersImport()
    goalie_retired = nhlpd.PlayersImport()

    # Connor Bedard
    skater_current = skater_current.queryNHLupdateDB(player_id=8484144)
    # Jay Bouwmeester
    skater_retired = skater_retired.queryNHLupdateDB(player_id=8470151)
    # Thatcher Demko
    goalie_current = goalie_current.queryNHLupdateDB(player_id=8477967)
    # Curtis Joseph
    goalie_retired = goalie_retired.queryNHLupdateDB(player_id=8448382)
