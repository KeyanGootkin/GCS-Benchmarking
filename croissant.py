import numpy as np
import pandas as pd
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
from time import mktime, strptime
from bisect import bisect
import os
from re import search
from glob import glob


def v_calc(h1, h2, deltat):
    """
    Takes the starting and ending heights of the CME and the time difference
    between the two measurements and calculates velocity.

    Parameters
    ----------
    h1 : float or string
        Starting height of the CME

    h2 : float or string
        Ending height of the CME

    deltat : float or string
        Time difference between the measurements of h1 and h2

    Returns
    ----------
    v : float
        velocity of the CME
    """
    # Radius of the sun in km, used for unit conversion
    Rsun = 695508
    # find the change in height of the CME in km and time in seconds
    deltah = (float(h2) - float(h1)) * Rsun
    deltat = float(deltat) * 60
    # calculates velocity
    v = deltah / deltat
    return(v)


def find_v():
    """
    Querries the user, asking for h1, h2, and deltat (starting/ending heights
    of the CME and the time difference) and returns these as floats.

    Returns
    ----------
    h1 : float
        Starting height of the CME

    h2 : float
        Ending height of the CME

    deltat : float
        Time difference between the measurements of h1 and h2
    """
    # Queries user for starting time, ending time, and change in time
    h1 = float(input("What is the starting height? "))
    h2 = float(input("What is the ending height? "))
    deltat = float(input("What is the time difference in minutes? "))
    # Calculate and print the velocity
    print("Velocity: " + str(v_calc(h1, h2, deltat)))
    # return starting height, ending height and change in time
    return(h1, h2, deltat)


def find_many_v():
    """
    Querries the user, asking for h1, h2, and deltat (starting/ending heights
    of the CME and the time difference) several times, and returns a list of the
    values collected/derived in this process.

    Returns
    ----------
    v_list : list
        a list of all velocities calculated

    t_list : list
        a list of times, starting at 0, and adding deltat at each step.

    h_list : list
        a list of CME heights
    """
    # start empty lists for velocity, time and height
    v_list = []
    t_list = []
    h_list = []
    # start time at 0 for the loop
    time = 0
    # Continue to repeat the steps below until the "break" condition is met
    while True:
        # Queries user for start height, end height and change in time
        h1, h2, deltat = find_v()
        # append the starting height and time to their lists, and calculate velocity and append to its list
        h_list.append(float(h1))
        v_list.append(v_calc(h1, h2, deltat))
        t_list.append(time)
        # add the change in time to the time counter
        time += float(deltat)
        print(v_list)
        print(t_list)
        # if the user types 'exit' then this breaks the data collection loop
        if input("Enter 'exit' to end measurement collection: ").lower() == 'exit':
            break
    # Since the above loop only adds the starting height and time, the next two lines
    # will add the final time and height to the appropriate lists
    t_list.append(time)
    h_list.append(float(h2))
    return(v_list, t_list, h_list)


def line_fit_cme():
    """
    Querries the user, asking for h1, h2, and deltat (starting/ending heights
    of the CME and the time difference) several times, and returns a list of the
    values collected in this process.

    Returns
    ----------
    time_list : list
        a list of times, starting at 0, and adding deltat at each step.

    height_list : list
        a list of CME heights
    """
    # start time at 0, and the time/height lists as empty
    time, time_list, height_list = 0, [], []
    # Loop through the data collection loop below until the user wants to exit
    while True:
        # Ask for height
        height_list.append(float(input("Height: ")))
        # append current time then add whatever the user wants to the total
        time_list.append(time)
        time += float(input("What is the time difference to the next frame? "))
        # check to see if the user is done
        if input("Enter 'exit' to end measurement collection: ").lower() == 'exit':
            break
    return(time_list, height_list)


def weird_date(zulu_date):
    """
    Takes a date in Zulu format, and converts it to a weird date, (roughly)
    the number of days since the beginning of the year.

    Parameters
    ----------
    zulu_date : string
        Date and time in the format "YYYY-MM-DDTHH:MMZ"

    Returns
    ----------
    Day : integer
        Very roughly the number of days since the beginning of that year.
    """
    # Returns number of days since the beginning of the year, roughly
    days = 0
    days += (int(zulu_date[5:7]) * 30 + int(zulu_date[8:10]))
    return(days)


def weird_time(zulu_time):
    """
    Takes a date in Zulu format, and converts it to a weird time, (roughly)
    the number of minutes since the beginning of the year.

    Parameters
    ----------
    zulu_time : string
        Date and time in the format "YYYY-MM-DDTHH:MMZ"

    Returns
    ----------
    time : integer
        Very roughly the number of minutes since the beginning of that year.
    """
    # returns the number of minutes since the beginning of the year, roughly
    time = 0
    time += (int(zulu_time[11:13]) * 60) + int(zulu_time[14:16])
    time += weird_date(zulu_time) * 24 * 60
    return(time)


def z_to_weird(zulu_times_list):
    """
    Takes a list of dates in Zulu format, and converts it to a list of weird times,
    (roughly) the number of minutes since the beginning of the year.

    Parameters
    ----------
    zulu_times_list : list
        Dates and times in the format "YYYY-MM-DDTHH:MMZ"

    Returns
    ----------
    weird_times_list : list
        A list where every index is very roughly the number of minutes since the
        beginning of that year.
    """
    # translates zulu time to weird time
    weird_times_list = []
    # for every zulu time in the list, translate to weird time
    for t in zulu_times_list:
        weird_times_list.append(weird_time(t))
    # normalize every weird time so that it is self consistent
    weird_times_list = np.array(weird_times_list) - min(weird_times_list)
    return(weird_times_list)


def add_zulu(start_zulu, added_time):
    """
    Takes a date and time in Zulu format and adds a number of minutes before
    converting back to Zulu time

    Parameters
    ----------
    start_zulu : string
        Starting date and time in the format "YYYY-MM-DDTHH:MMZ"

    added_time : integer
        The number of minutes you would like to add

    Returns
    ----------
    end_zulu : string
        Ending date and time in the format "YYYY-MM-DDTHH:MMZ"
    """
    # Reads in the mins, hours, days, months and years from the standard Zulu time
    # format 'YYYY-MM-DDThh:mmZ'
    mins = int(start_zulu[14:16])
    hours = int(start_zulu[11:13])
    days = int(start_zulu[8:10])
    month = int(start_zulu[5:7])
    year = int(start_zulu[0:4])
    # add the number of minutes specified
    mins += added_time
    # Carry over extra minutes into the hours place
    while mins >= 60:
        hours += 1
        mins -= 60
    # Carry over extra hours into the days place
    while hours >= 24:
        days += 1
        hours -= 24
    chars = ''
    for i in str(mins):
        if i == '.':
            break
        chars += i
    mins = chars
    # These many if statements just check to see if '1' needs to be '01' and whatnot
    if len(str(mins)) == 1:
        mins = "0" + str(mins)
    if len(str(hours)) == 1:
        hours = "0" + str(hours)
    if len(str(days)) == 1:
        days = "0" + str(days)
    if len(str(month)) == 1:
        month = "0" + str(month)
    # take all the integers and turn them into the correct strings w/ Zulu format
    end_zulu = str(year) + '-' + str(month) + '-' + str(days) + \
        'T' + str(hours) + ':' + str(mins) + 'Z'
    # if the days are greater than or equal to 31 then something mayyyy be wrong
    if int(days) >= 31:
        # ask the user if the date is wrong
        answer = input(
            "WARNING: Zulu date may have crossed into a new month. Does this date look correct? (type y or n) %s: " % (end_zulu))
        if answer == 'n':
            # if the end zulu is wrong, make the user do the dang math
            end_zulu = input("Please calculate the end date, the start date was " + str(
                start_zulu) + ' and you must add ' + str(added_time) + ' minutes. ')
    return(end_zulu)


def funct(x, s, i):
    # This is just for cme_line_fit's curve_fit, it needs to be a pre-defined function for some reason
    return(s * x + i)


def cme_line_fit(ts, hs, return_slope=False):
    """
    Takes a date and time in Zulu format and adds a number of minutes before
    converting back to Zulu time

    Parameters
    ----------
    ts : list
        Time
    Returns
    ----------
    end_zulu : string
        Ending date and time in the format "YYYY-MM-DDTHH:MMZ"
    """
    Rsun = 695508
    popt, pcov = curve_fit(funct, ts, hs)
    s, i = popt[0], popt[1]
    # Maybe plot
    if return_slope == False:
        # make x values to plot line regression against
        x = np.linspace(min(ts), max(ts), 10)
        # scatter plot the real data
        plt.scatter(ts, hs)
        # line plot the line of best fit
        plt.plot(x, (s * x + i), 'r')
        # put the slope (velocity) in the title
        plt.title("Velocity (km/s): " + str(g))
        # Show that figure!
        plt.show()
    # Maybe return the slope
    elif return_slope == True:
        return(s * Rsun / 60)


def find_cme_start(start_t, start_h, velocity):
    """
    Takes measurements of a CME from coronagraph imagery and calculates when the
    CME will reach 21.5 solar radii, where the ENLIL model takes over.

    Parameters
    ----------
    start_t : string
        Starting date and time from which you would like to calculate the CMEs
        time at 21.5 solar radii, in the format "YYYY-MM-DDTHH:MMZ". Note that
        this time must match with the start_h below. It is advised that this
        starting time be as late as possible so that errors introduced by the
        calculated velocity are minimized.

    start_h : float or int
        Starting CME height in solar radii from which you would like to calculate
        the CMEs time at 21.5 solar radii. note that this height must match the
        starting time listed above.

    velocity : float or int
        Velocity of the CME in solar radii per minute.

    Returns
    ----------
    end_time : string
        CMEs arrival at 21.5 solar radii in the format "YYYY-MM-DDTHH:MMZ"
    """
    # Convert velocity from km/s to Rsun/min
    velocity = (velocity / 695508) * 60
    # Calculate number of minutes until CME reaches ENLIL inner boundary assuming
    # Note: start_t and start_h should be for the latest measurement, so that
    # Errors are minimized.
    delta_t = (21.5 - start_h) / velocity
    # add delta_t to the start_time. Outputs in Zulu time
    end_time = add_zulu(start_t, delta_t)
    return(end_time)


def cr2sh(date, carrington):    
    """
    Takes a date and Carrington longitude and returns a Stonyhurst longitude.
    Converts carrington to stonyhurst

    Parameters
    ----------
    date : string
        Date and time in the format "YYYY-MM-DDTHH:MM:00"

    carrington : float
        Carrington longitude.

    Returns
    ----------
    stonyhurst : float
        Stonyhurst longitude.
        The date of the longitude measurement in the format "YYYY-MM-DDTHH:MMZ"

    carrington : float
        Longitude in carrington coordinates.

    Returns
    ----------
    stonyhurst : float
        Longitude in stonyhurst coordinates.
    """
    # grab dates
    carrots = np.loadtxt(
        str(os.path.dirname(os.path.realpath(__file__))) + "/carrots.txt")
    # turn input date into a mathable value
    datemk = mktime(strptime(date, "%Y-%m-%dT%H:%M:00"))
    # identify start and end times for the rotation
    rotation = bisect(carrots, datemk)
    start = carrots[rotation - 1]
    end = carrots[rotation]
    # the math part
    stonyhurst = carrington - 360 * (1 - (datemk - start) / (end - start))
    # make sure results are in bounds
    if stonyhurst < 0:
        return stonyhurst + 360
    else:
        return stonyhurst


def sh2cr(date, stonyhurst):
    """
    Takes a date and Stonyhurst longitude and returns a Carrington longitude.
    Converts stonyhurst to carrington

    Parameters
    ----------
    date : string
        Date and time in the format "YYYY-MM-DDTHH:MM:00"

    carrington : float
        Stonyhurst longitude.

    Returns
    ----------
    carrington : float
        Carrington longitude.

        The date of the longitude measurement in the format "YYYY-MM-DDTHH:MMZ"

    stonyhurst : float
        Longitude in stonyhurst coordinates.

    Returns
    ----------

    carrington : float
        Longitude in carrington coordinates.
    """
    carrots = np.loadtxt(
        str(os.path.dirname(os.path.realpath(__file__))) + "/carrots.txt")
    # re-commenting this is beneath my dignity
    datemk = mktime(strptime(date, "%Y-%m-%dT%H:%M:00"))
    rotation = bisect(carrots, datemk)
    start = carrots[rotation - 1]
    end = carrots[rotation]
    # note plus sign
    carrington = stonyhurst + 360 * (1 - (datemk - start) / (end - start))
    if carrington > 360:
        return carrington - 360
    else:
        return carrington


def cme_match(*directories):

    """
    Looks at all .rt files in the given directory or directories and groups
    them up by CME.

    Parameters
    ----------
    directories : string
        0 or more directory names. If 0, cme_match() finds all appropriately
        named .rt files in /data/[acjkr]data/.

    Returns
    ----------
    matches : list
        List of lists of filenames.
    """

    files, cmes, matches = [], [], []

    # if no arguments grab all files, otherwise grab specified files
    if len(directories) == 0:
        files.extend(glob(str(os.path.dirname(os.path.realpath(__file__))) +
                          "/data/[acjkr]data/[0-9]WLRT_[1-2]???-??-??_????.rt"))
    else:
        for directory in directories:
            files.extend(glob(str(os.path.dirname(os.path.realpath(
                __file__))) + "/" + directory + "/[0-9]WLRT_[1-2]???-??-??_????.rt"))

    # pull out just the filenames
    for file in files:
        cmes.append(file[-17:-7])

    # massage this list so it's tidier
    cmes = list(set(cmes))
    cmes.sort()

    # list files for each CME
    for cme in cmes:
        matches.append([file for file in files if cme in file])

    return matches


def cme_times(times):
    """
    Takes a list of frame timestamps and returns minutes from zero, where zero
    is the earliest timstamp.

    Parameters
    ----------
    times : list
        2 or more timestamps in the format YYYY-MM-DDTHH:MM:00.

    Returns
    ----------
    minutes : list
        Minutes from zero.
    """
    timesmk = []
    minutes = [0]

    if len(times) <= 1:
        return "cme_times() requires at least two values."
    else:
        for time in times:
            timesmk.append(mktime(strptime(time, "%Y-%m-%dT%H:%M:00")))
        timesmk_index = 1
        for mk in timesmk:
            if len(timesmk) - 1 >= timesmk_index:
                minutes.append(
                    ((timesmk[timesmk_index] - mk) / 60) + minutes[len(minutes) - 1])
                timesmk_index += 1
            else:
                break

    return minutes


def make_eUCLID(cmes_list):
    """
    Takes a list of GCS CME output file paths, averages all of the measurements
    of the same CME and outputs a dataframe containing average time, longitude,
    latitude, tilt angle, velocity, ascpect ratio, half angle, and time at 21.5
    solar radii for each CME.

    Parameters
    ----------
    cmes_list : list or array
        A nested list where it would have lists inside of it, each sublist
        has multiple measurements of the same CME. ie [[m1,m2,m3,m4],[m1,m2]]
        would have 2 cmes. CME 1 has four measurements and CME 2 has 2 measurements.
        Each measurement is a GCS output file.

    Returns
    ----------
    all_cmesdf : pandas DataFrame
        A data frame containing time, longitude, latitude, tilt angle, velocity,
        ascpect ratio, and half angle for each measurement of each CME.

    cmedf : pandas DataFrame
        a DataFrame containing average time, longitude, latitude, tilt angle,
        velocity, ascpect ratio, half angle, and time at 21.5 solar radii for
        each CME.
    """
    # Create empty dataframes to populate later
    cmedf = pd.DataFrame()
    all_cmesdf = pd.DataFrame()
    # Loop through each cme in the list of cmes
    for cme in cmes_list:
        tempdf = pd.DataFrame()
        # loop through each measurement of the cme
        for mf in cme:
            # Read the measurement into a dataframe
            measurement = pd.read_csv(mf, names=["Time", "Lon", "Lat", "ROT", "Height", "Ratio", "Half Angle"],
                                      delim_whitespace=True, header=0, usecols=[0, 1, 2, 3, 4, 5, 6])
            # Turn zulu into mathable times
            times_list = cme_times(measurement["Time"])
            # calculate velocity
            velocity = cme_line_fit(
                times_list, measurement["Height"], return_slope=True)
            # Use velocity to calculate the time at 21.5 Rs
            enlilstart = find_cme_start(measurement["Time"][len(
                measurement["Time"]) - 1], measurement["Height"][len(measurement["Height"]) - 1], velocity)
            # find the average of each parameter in one measurement
            ave_measurement = measurement.mean()
            # turn the averages into a dataframe so that it can easily be appended
            ave_measurement = pd.DataFrame({"Time": measurement["Time"][len(measurement["Time"]) - 1], 'Lon': cr2sh(measurement["Time"][len(measurement["Time"]) - 1], ave_measurement['Lon']), 'Lat': ave_measurement['Lat'], 'ROT': ave_measurement['ROT'],
                                            "Velocity": velocity, 'Ratio': ave_measurement['Ratio'], 'Half Angle': ave_measurement['Half Angle'], "Time at 21.5": enlilstart[:16] + "Z"}, index=[0])
            # add this measurement to the df containing all individual measurements
            all_cmesdf = all_cmesdf.append(ave_measurement, ignore_index=True)
            tempdf = tempdf.append(ave_measurement, ignore_index=True)
        ave_of_temp = tempdf.mean()
        transferdf = pd.DataFrame({"Time": ave_measurement["Time"], 'Lon': ave_of_temp["Lon"], 'Lat': ave_of_temp['Lat'], 'ROT': ave_of_temp['ROT'],
                                   "Velocity": ave_of_temp["Velocity"], 'Ratio': ave_of_temp['Ratio'], 'Half Angle': ave_of_temp['Half Angle'], "Time at 21.5": find_cme_start(tempdf["Time"][len(tempdf["Time"]) - 1], measurement["Height"][len(measurement["Height"]) - 1], ave_of_temp["Velocity"])}, index=[0])
        cmedf = cmedf.append(transferdf, ignore_index=True)
    cmedf.to_csv(str(os.path.dirname(os.path.realpath(__file__))
                     ) + '/eUCLID.txt', sep=":")
    all_cmesdf.to_csv(str(os.path.dirname(os.path.realpath(__file__))
                          ) + '/all_measurements.txt', sep=":")
    return(all_cmesdf, cmedf)


def make_hist(std_list, range_list, name, units, figdir, labels):
    """
    Parameters
    ----------
    std_list : list or array
        list of standard deviations you wish to plot on the histogram

    range_list : list or array
        list of ranges you wish to plot on the histogram

    name : string
        Name of the parameter which is being plotted

    units : dictionary
        Dictionary where the key is the name and each name is linked to the
        proper units for that parameter

    figdir : string
        Full path to the directory in which you would like to store the histogram

    labels : dictionary
        Dictionary where the key is the name and each name is linked to the
        proper name of the parameter which you would like to appear on the
        final histograms.
    """
    if labels[name] == "Tilt Angle":
        b = np.arange(0, max(range_list) + 20, 20)

    elif labels[name] == "Half Angle":
        b = np.arange(0, max(range_list) + 5, 5)

    elif units[name] == "(Degrees)":
        #b = int(max(range_list)/2)
        b = np.arange(0, max(range_list) + 1, 2)

    elif units[name] == '':
        #b = int(max(range_list)/0.1)
        b = np.arange(0, max(range_list) + 0.1, 0.1)
    else:
        b = np.arange(0, max(range_list) + 50, 50)
    plt.hist(std_list, bins=b, alpha=0.5,
             label='Standard Deviation', color="#FFCD8C")
    plt.hist(range_list, bins=b, alpha=0.3, label='Range', color='#74A7C4')
    plt.title("Standard Deviation and Range of " +
              labels[name], size=18, fontname='Verdana')
    plt.xlabel(units[name], size=14, fontname='Verdana')
    plt.ylabel("Frequency", size=14, fontname='Verdana')
    plt.xticks(fontsize=15, fontname='Verdana')
    plt.yticks(fontsize=15, fontname='Verdana')
    plt.legend(loc='best')
    plt.savefig(figdir + "std_range_hists/" +
                name + "_hist.png", overwrite=True, dpi=500)
    plt.clf()


def make_scatter(std_list, range_list, mean_list, name, units, figdir, labels):
    """
    Parameters
    ----------
    std_list : list or array
        list of standard deviations you wish to plot on the scatter plots

    range_list : list or array
        list of ranges you wish to plot on the scatter plots

    mean_list : list or array
        list of means you wish to plot on the scatter plots

    name : string
        Name of the parameter which is being plotted

    units : dictionary
        Dictionary where the key is the name and each name is linked to the
        proper units for that parameter

    figdir : string
        Full path to the directory in which you would like to store the scatter
        plot

    labels : dictionary
        Dictionary where the key is the name and each name is linked to the
        proper name of the parameter which you would like to appear on the
        final scatter plots.
    """
    plt.scatter(mean_list, std_list, color='#2F454F',
                label="Standard Deviation")
    plt.scatter(mean_list, range_list, color="#F7941D", label="Range")
    if name == 'Half Angle':
        plt.xlim(8, 39)
    plt.xlabel("Mean " + units[name], size=14, fontname='Verdana')
    plt.ylabel(units[name], size=14, fontname='Verdana')
    plt.xticks(fontsize=15, fontname='Verdana')
    plt.yticks(fontsize=15, fontname='Verdana')
    plt.title("Standard Deviation and Range of " +
              labels[name], size=18, fontname='Verdana')
    plt.legend(loc=1)
    plt.savefig(figdir + "std_range_scatters/range_" +
                name + "_scatter.png", overwrite=True, dpi=500)
    plt.clf()


def plot_cmes(cmedf, all_cmesdf, dates, units, labels, figdir):
    """
    Parameters
    ----------
    cmedf : pandas DataFrame
        a DataFrame containing average time, longitude, latitude, tilt angle,
        velocity, ascpect ratio, half angle, and time at 21.5 solar radii for
        each CME.

    all_cmesdf : pandas DataFrame
        A data frame containing time, longitude, latitude, tilt angle, velocity,
        ascpect ratio, and half angle for each measurement of each CME.

    dates : list or array
        list or array containing strings which are the dates of the CMEs in the
        format "YYYY-MM-DD".

    units : dictionary
        Dictionary where the key is the name and each name is linked to the
        proper units for that parameter

    labels : dictionary
        Dictionary where the key is the name and each name is linked to the
        proper name of the parameter which you would like to appear on the
        final scatter plots.

    figdir : string
        Full path to the directory in which you would like to store the scatter
        plot
    """
    normarray = []
    for name in all_cmesdf.columns:
        if all_cmesdf[name].dtypes != 'object':
            mean_list, std_list, range_list = [], [], []
            name_norm_array = []
            new_norm = pd.Series()
            for base_time in dates:
                temp_storage = []
                for ind_time, x in zip(all_cmesdf["Time"], all_cmesdf[name]):
                    if base_time[:10] == ind_time[:10]:
                        temp_storage.append(x)
                mean_p = np.mean(temp_storage)
                mean_list.append(mean_p)
                std_p = np.std(temp_storage)
                std_list.append(std_p)
                range_p = max(temp_storage) - min(temp_storage)
                range_list.append(range_p)
                if name == "Velocity":
                    norms = ((np.array(temp_storage) - np.mean(np.array(temp_storage))
                              ) / np.mean(np.array(temp_storage))) * 100
                else:
                    norms = (np.array(temp_storage) -
                             np.mean(np.array(temp_storage)))
                for i in norms:
                    name_norm_array.append(i)
                normarray.append(norms)
            make_hist(std_list, range_list, name, units, figdir, labels)
            if name == "Velocity" or name == "Half Angle":
                make_scatter(std_list, range_list, mean_list,
                             name, units, figdir, labels)
