import nhlpd


# for now, main serves as a program script to test functions
def main():
    shifts = nhlpd.ShiftsImport()
    result = shifts.queryNHLupdateDB()

    return result


main()
