import nhlpd


# for now, main serves as a program script to test functions
def main():
    rosters = nhlpd.RostersImport()
    result = rosters.queryNHLupdateDB()

    return result


main()
