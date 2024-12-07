# from datetime import datetime
import nhlpd

# for now, main serves as a program script to test functions
if __name__ == "__main__":
    scheduler = nhlpd.Scheduler()

    scheduler.checkTeams()
    scheduler.checkSeasons()
    scheduler.checkGames()
    scheduler.checkGameCenters()
    scheduler.checkRosters()
    scheduler.checkPlayers()

    print("hej")
