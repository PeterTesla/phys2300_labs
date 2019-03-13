'''
Assignment to learn how to interpolate data1
'''
import sys
import matplotlib.pyplot as plt
import numpy as np
import scipy
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

def zero_time(time):
    '''
    Take a list of time data points and make the first point t = 0, then adjust all subsequent points
    '''
    init = time[0]
    time[:] = [t - init for t in time]

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

    harbor_data['wx_temperatures'] = []
    harbor_data['wx_times'] = []

    with open(wx_file, newline = '') as data:
        stuff = csv.reader(data, delimiter=',')
        next(stuff)

        for each in stuff:
            wx_data.append(each)

    for each in wx_data:
        wx_times.append( get_hours(each[1]) )

    zero_time(wx_times)

    for each in wx_data:
        wx_temperatures.append( float(each[3]) )

    last = 0
    for i, time in enumerate(wx_times):
        if time < harbor_data['gps_times'][-1]:
            if (last-wx_temperatures[i])/wx_temperatures[i] > .25:
                harbor_data['wx_temperatures'].append(last)
            else:
                harbor_data['wx_temperatures'].append( wx_temperatures[i] )

            last = wx_temperatures[i]
            harbor_data['wx_times'].append( wx_times[i] )

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
    zero_time(gps_times)

    for each in gps_data:
        gps_altitude.append( float(each[6]) )    

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

    harbor_data['crltd_alt_up'] = []
    harbor_data['crltd_temp_up'] = []
    harbor_data['crltd_alt_down'] = []
    harbor_data['crltd_temp_down'] = []

    interp_altitude = np.interp(harbor_data['wx_times'], harbor_data['gps_times'], harbor_data['gps_altitude'])

    for i, alt in enumerate(interp_altitude):
        dydt = (alt - interp_altitude[i-1])/(harbor_data['wx_times'][i] - harbor_data['wx_times'][i-1])
        if dydt > 0:
            harbor_data['crltd_alt_up'].append(alt)
            harbor_data['crltd_temp_up'].append(harbor_data['wx_temperatures'][i])
        else:
            harbor_data['crltd_alt_down'].append(alt)
            harbor_data['crltd_temp_down'].append(harbor_data['wx_temperatures'][i])

    del harbor_data['crltd_temp_down'][0]
    del harbor_data['crltd_alt_down'][0]




def plot_figs(harbor_data):
    """
    Plot 2 figures with 2 subplots each.
    :param harbor_data: A dictionary to collect data.
    :return: nothing
    """
    fig1, [temp, altitude] = plt.subplots(2, 1, sharex=True)

    temp.set_title("Harbor Flight Data")
    temp.plot(harbor_data['wx_times'], harbor_data['wx_temperatures'], color='black')
    temp.set_ylabel("Temperature, (F)")

    temp.set_ylim(-50,80)

    altitude.plot(harbor_data['gps_times'], harbor_data['gps_altitude'], color='black')
    altitude.set_ylabel("Altitude, (Ft)")
    plt.xlabel("Time (H)")

    fig2, [rising,falling] = plt.subplots(1,2, sharey=True)

    rising.set_title("Harbor Ascent Data")
    rising.plot(harbor_data['crltd_temp_up'],harbor_data['crltd_alt_up'], color='black')
    rising.set_ylabel("Altitude (ft)")
    rising.set_xlabel("Temperature (F)")

    falling.set_title("Harbor Descent Data")
    falling.plot(harbor_data['crltd_temp_down'],harbor_data['crltd_alt_down'], color='black')
    falling.set_xlabel( "Temperature (F)" )

    plt.show()


def main():
    """
    Main function
    :return: Nothing
    """
    harbor_data = {}

    wx_file = sys.argv[1]                   # first program input param as filepath
    gps_file = sys.argv[2]                  # second program input param as filepath

    read_gps_data(gps_file, harbor_data)    # collect gps dataw
    read_wx_data(wx_file, harbor_data)      # collect weather data

    interpolate_wx_from_gps(harbor_data)    # calculate interpolated data
    plot_figs(harbor_data)                  # display figures


if __name__ == '__main__':

    main()
    exit(0)
