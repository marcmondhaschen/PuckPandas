# from datetime import datetime
import nhlpd

# for now, main serves as a program script to test functions
if __name__ == "__main__":
    tableLog = nhlpd.ImportTableUpdateLog()

    scheduler = nhlpd.Scheduler()

    scheduler.checkTeamsImport()
    scheduler.checkSeasonsImport()
    scheduler.checkGamesImport()
    scheduler.checkGameCentersImport()
    scheduler.checkRostersImport()
    scheduler.checkPlayersImport()

    print("hej")
