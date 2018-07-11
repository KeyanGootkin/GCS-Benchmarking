import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt


def v_calc(h1,h2,deltat):
    #Radius of the sun in km, used for unit conversion
    Rsun = 695508
    #find the change in height of the CME in km and time in seconds
    deltah = (float(h2)-float(h1))*Rsun
    deltat = float(deltat)*60
    #calculates velocity
    v = deltah/deltat
    return(v)

def find_v():
    #Queries user for starting time, ending time, and change in time
    h1 = float(input("What is the starting height? "))
    h2 = float(input("What is the ending height? "))
    deltat = input("What is the time difference in minutes? ")
    #Calculate and print the velocity
    print("Velocity: " + str(v_calc(h1,h2,deltat)))
    #return starting height, ending height and change in time
    return(h1,h2,deltat)

def find_many_v():
    #start empty lists for velocity, time and height
    v_list = []
    t_list = []
    h_list = []
    #start time at 0 for the loop
    time = 0
    #Continue to repeat the steps below until the "break" condition is met
    while True:
        #Queries user for start height, end height and change in time
        h1,h2,deltat = find_v()
        #append the starting height and time to their lists, and calculate velocity and append to its list
        h_list.append(float(h1))
        v_list.append(v_calc(h1,h2,deltat))
        t_list.append(time)
        #add the change in time to the time counter
        time += float(deltat)
        print(v_list)
        print(t_list)
        #if the user types 'exit' then this breaks the data collection loop
        if input("Enter 'exit' to end measurement collection: ").lower() == 'exit':
            break
    #Since the above loop only adds the starting height and time, the next two lines
    #will add the final time and height to the appropriate lists
    t_list.append(time)
    h_list.append(float(h2))
    return(v_list,t_list,h_list)

def line_fit_cme():
    #start time at 0, and the time/height lists as empty
    time,time_list,height_list = 0,[],[]
    #Loop through the data collection loop below until the user wants to exit
    while True:
        #Ask for height
        height_list.append(float(input("Height: ")))
        #append current time then add whatever the user wants to the total
        time_list.append(time)
        time += float(input("What is the time difference to the next frame? "))
        #check to see if the user is done
        if input("Enter 'exit' to end measurement collection: ").lower() == 'exit':
            break
    return(time_list,height_list)

def weird_date(zulu_date):
    #Returns number of days since the beginning of the year, roughly
    days = 0
    days += (int(zulu_date[5:7]) * 30 + int(zulu_date[8:10]))
    return(days)


def weird_time(zulu_time):
    #returns the number of minutes since the beginning of the year, roughly
    time = 0
    time += (int(zulu_time[11:13]) * 60) + int(zulu_time[14:16])
    time += weird_date(zulu_time) * 24 * 60
    return(time)


def z_to_weird(zulu_times_list):
    #translates zulu time to weird time
    weird_times_list = []
    #for every zulu time in the list, translate to weird time
    for t in zulu_times_list:
        weird_times_list.append(weird_time(t))
    #normalize every weird time so that it is self consistent
    weird_times_list = np.array(weird_times_list) - min(weird_times_list)
    return(weird_times_list)

def add_zulu(start_zulu, added_time):
    #Reads in the mins, hours, days, months and years from the standard Zulu time
    #format 'YYYY-MM-DDThh:mmZ'
    mins = int(start_zulu[14:16])
    hours = int(start_zulu[11:13])
    days = int(start_zulu[8:10])
    month = int(start_zulu[5:7])
    year = int(start_zulu[0:4])
    #add the number of minutes specified
    mins += added_time
    #Carry over extra minutes into the hours place
    while mins >= 60:
        hours += 1
        mins -= 60
    #Carry over extra hours into the days place
    while hours >= 24:
        days += 1
        hours -= 24
    #These many if statements just check to see if '1' needs to be '01' and whatnot
    if len(str(mins)) == 1:
        mins = "0" + str(mins)
    if len(str(hours)) == 1:
        hours = "0" + str(hours)
    if len(str(days)) == 1:
        days = "0" + str(days)
    if len(str(month)) == 1:
        month = "0" + str(month)
    #take all the integers and turn them into the correct strings w/ Zulu format
    end_zulu = str(year) + '-' + str(month) + '-' + str(days) + \
        'T' + str(hours) + ':' + str(mins) + 'Z'
    #if the days are greater than or equal to 31 then something mayyyy be wrong
    if int(days) >= 31:
        #ask the user if the date is wrong
        answer = input(
            "WARNING: Zulu date may have crossed into a new month. Does this date look correct? (type y or n) %s: " % (end_zulu))
        if answer == 'n':
            #if the end zulu is wrong, make the user do the dang math
            end_zulu = input("Please calculate the end date, the start date was " + str(
                start_zulu) + ' and you must add ' + str(added_time) + ' minutes. ')
    return(end_zulu)

def funct(x,s,i):
    #This is just for cme_line_fit's curve_fit, it needs to be a pre-defined function for some reason
    return(s*x+i)

def cme_line_fit(ts,hs):
    #use scipy's curve fit to optimize the slope and intercept of the line
    popt,pcov = curve_fit(funct,ts,hs)
    s,i = popt[0],popt[1]
    #make x values to plot line regression against
    x = np.linspace(min(ts),max(ts),10)
    #scatter plot the real data
    plt.scatter(ts,hs)
    #line plot the line of best fit
    plt.plot(x,(s*x+i),'r')
    #put the slope (velocity) in the title
    plt.title("Velocity (km/s): " +str(s*Rsun/60))
    #Show that figure!
    plt.show()
