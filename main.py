import DBCreation.connection as dbcon
import DBCreation.tables as dbtab
import Utils.insertData as utidat
import Utils.graphs as graphs
import pandas as pd
import numpy as np
from sko.GA import GA

def main():
    """
        The main function that orchestrates the execution of the program.

    """
    # first time setup
    firstTimeSetup()
    # generate graphs
    generateGraphs()


def firstTimeSetup():
    """
        Performs the first-time setup for the program, including testing the database connection,
        creating tables, and inserting data into the database.

    """
    # test the database connection
    dbcon.testConnection()
    # create the tables if they don't exist in the database
    dbtab.createTables()
    # insert the data in the database
    utidat.insertDataInDB()


def generateGraphs():
    """
        Generates various graphs, including scatter plots, time series plots, and ARIMA training and split.

    """
    # generate the scatter plot
    graphs.getScatterPlot()
    # generate the time series plot
    graphs.getTimeSeries()
    # perform the ARIMA training and split
    graphs.getARIMATrainingSplit()


if __name__ == '__main__':
    main()




