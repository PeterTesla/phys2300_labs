'''
Assignment to learn how to interpolate data1
'''
import sys
# import matplotlib.pyplot as plt
# import numpy as np
# import scipy
import csv

def get_hours(time_str):
    '''
    Takes in a H:M:S formatted time and converts to decimal hours
    '''
    try:
        h,m,s = time_str.split(':')
        return (int(h) + int(m)/60 + int(s)/3600)
    except:
        return "NaN"

def read_wx_data(wx_file, harbor_data):
    """
    Read temperature and time data from file.
    Populates the harbor_data dictionary with two lists: wx_times and wx_temperatures
    :param wx_file: File object with data
    :param harbor_data: A dictionary to collect data.
    :return: Nothing
    """

    wx_data =[]
    wx_temperatures = []
    wx_times = []

    with open(wx_file, newline = '') as data:
        stuff = csv.reader(data, delimiter=',')
        next(stuff)

        for each in stuff:
            wx_data.append(each)

    for each in wx_data:
        wx_times.append( get_hours(each[1]) )

    for each in wx_data:
        wx_temperatures.append( each[3] )

    harbor_data['wx_temperatures'] = wx_temperatures
    harbor_data['wx_times'] = wx_times



def read_gps_data(gps_file, harbor_data):
    """
    Read gps and altitude data from file.
    Populates the harbor_data dictionary with two lists: gps_times and gps_altitude
    :param gps_file: File object with gps data
    :param harbor_data: A dictionary to collect data.
    :return: Nothing
    """
    gps_data =[]
    gps_altitude = []
    gps_times = []

    with open(gps_file, newline = '') as data:
        stuff = csv.reader(data, delimiter='\t')
        for _ in range(2): next(stuff)

        for each in stuff:
            gps_data.append(each)

    for each in gps_data:
        gps_times.append( get_hours(each[0] + ':' + each[1] + ':' + each[2]) )    

    for each in gps_data:
        gps_altitude.append( each[6] )    

    harbor_data['gps_altitude'] = gps_altitude
    harbor_data['gps_times'] = gps_times



def interpolate_wx_from_gps(harbor_data):
    """
    Compute wx altitudes by interpolating from gps altitudes
    Populates the harbor_data dictionary with four lists:
        1) wx correlated altitude up
        2) wx correlated temperature up
        3) wx correlated altitude down
        4) wx correlated temperature down
    :param harbor_data: A dictionary to collect data.
    :return: Nothing
    """


    pass


def plot_figs(harbor_data):
    """
    Plot 2 figures with 2 subplots each.
    :param harbor_data: A dictionary to collect data.
    :return: nothing
    """

    

    pass


def main():
    """
    Main function
    :return: Nothing
    """
    harbor_data = {}


    wx_file = sys.argv[1]                   # first program input param as filepath
    gps_file = sys.argv[2]                  # second program input param as filepath

    read_wx_data(wx_file, harbor_data)      # collect weather data
    read_gps_data(gps_file, harbor_data)    # collect gps data

    #interpolate_wx_from_gps(harbor_data)    # calculate interpolated data
    #plot_figs(harbor_data)                  # display figures


if __name__ == '__main__':
    main()
    exit(0)
