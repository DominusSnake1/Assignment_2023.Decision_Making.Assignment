import Utils.connection as uticon
import Utils.tables as utitab
import Utils.insertData as utidat
import Utils.statistics as stats
import Utils.graphs as graphs


uticon.testConnection()
# utitab.createTables()
# utidat.insertDataInDB()

graphs.generateScatterPlot()
graphs.getTimeSeries()
graphs.getARIMATrainingSplit()
