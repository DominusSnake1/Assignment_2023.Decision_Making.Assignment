import Utils.connection as uticon
import Utils.tables as utitab
import Utils.insertData as utiran

uticon.testConnection()
utitab.createTables()
utiran.insertRandomUsers(20)
