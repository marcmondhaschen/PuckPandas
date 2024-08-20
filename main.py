import nhlpd


# for now, main serves as a program script to test functions
def main():
    teams = nhlpd.TeamsImport()
    result = teams.queryNHLupdateDB()
    return result


main()
