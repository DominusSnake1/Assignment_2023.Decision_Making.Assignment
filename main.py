import DBCreation.connection as dbcon
import DBCreation.tables as dbtab
import Utils.insertData as utidat
import Utils.graphs as graphs


def main():
    firstTimeSetup()
    generateGraphs()


def firstTimeSetup():
    dbcon.testConnection()
    dbtab.createTables()
    utidat.insertDataInDB()


def generateGraphs():
    graphs.getScatterPlot()
    graphs.getTimeSeries()
    graphs.getARIMATrainingSplit()


if __name__ == '__main__':
    main()
