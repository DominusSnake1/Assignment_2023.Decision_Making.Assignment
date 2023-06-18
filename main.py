import Utils.connection as uticon
import Utils.tables as utitab
import Utils.insertData as utidat
import Utils.statistics as stats
import Utils.graphs as graphs


def main():
    firstTimeSetup()

    graphs.generateScatterPlot()
    graphs.getTimeSeries()
    graphs.getARIMATrainingSplit()


def firstTimeSetup():
    uticon.testConnection()
    utitab.createTables()
    utidat.insertDataInDB()


if __name__ == '__main__':
    main()