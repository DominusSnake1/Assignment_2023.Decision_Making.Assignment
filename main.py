import Utils.connection as uticon
import Utils.tables as utitab
import Utils.insertData as utidat

uticon.testConnection()
utitab.createTables()
utidat.insertDataInDB()
