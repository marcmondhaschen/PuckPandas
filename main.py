import nhlpd


# for now, main serves as a program script to test functions
if __name__ == "__main__":
    teams = nhlpd.TeamsImport()
    result = teams.queryNHLupdateDB('STL')
    print(result)
