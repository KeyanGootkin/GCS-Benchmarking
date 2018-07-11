import numpy as np


def v_calc(h1,h2,deltat):
    Rsun = 695508
    deltah = (float(h2)-float(h1))*Rsun
    deltat = float(deltat)*60
    v = deltah/deltat
    return(v)

def find_v():
    h1 = float(input("What is the starting height? "))
    h2 = float(input("What is the ending height? "))
    deltat = input("What is the time difference in minutes? ")
    print("Velocity: " + str(v_calc(h1,h2,deltat)))
    return(h1,h2,deltat)

def find_many_v():
    v_list = []
    t_list = []
    h_list = []
    time = 0
    """halfangle = np.rad2deg(float(input("What is the half-angle? ")))
    kappa = float(input("What is the ratio? "))
    hratio = (1+np.tan2(halfangle))/(1-kappa)"""
    while True:
        h1,h2,deltat = find_v()
        h_list.append(float(h1))
        v_list.append(v_calc(h1,h2,deltat))
        t_list.append(time)
        time += float(deltat)
        print(v_list)
        print(t_list)
        if input("Enter 'exit' to end measurement collection: ").lower() == 'exit':
            break
    t_list.append(time)
    h_list.append(float(h2))
    return(v_list,t_list,h_list)

def line_fit_cme():
    time,time_list,height_list = 0,[],[]
    while True:
        height_list.append(float(input("Height: ")))
        time_list.append(time)
        time += float(input("What is the time difference to the next frame? "))
        if input("Enter 'exit' to end measurement collection: ").lower() == 'exit':
            break
    return(time_list,height_list)

def weird_date(zulu_date):
    days = 0
    days += (int(zulu_date[5:7]) * 30 + int(zulu_date[8:10]))
    return(days)


def weird_time(zulu_time):
    time = 0
    time += (int(zulu_time[11:13]) * 60) + int(zulu_time[14:16])
    time += weird_date(zulu_time) * 24 * 60
    return(time)


def z_to_weird(zulu_times_list):
    weird_times_list = []
    for t in zulu_times_list:
        weird_times_list.append(weird_time(t))
    weird_times_list = np.array(weird_times_list) - min(weird_times_list)
    return(weird_times_list)

def add_zulu(start_zulu, added_time):
    mins = int(start_zulu[14:16])
    hours = int(start_zulu[11:13])
    days = int(start_zulu[8:10])
    month = int(start_zulu[5:7])
    year = int(start_zulu[0:4])
    mins += added_time
    while mins >= 60:
        hours += 1
        mins -= 60
    while hours >= 24:
        days += 1
        hours -= 24
    if len(str(mins)) == 1:
        mins = "0" + str(mins)
    if len(str(hours)) == 1:
        hours = "0" + str(hours)
    if len(str(days)) == 1:
        days = "0" + str(days)
    if len(str(month)) == 1:
        month = "0" + str(month)
    end_zulu = str(year) + '-' + str(month) + '-' + str(days) + \
        'T' + str(hours) + ':' + str(mins) + 'Z'
    if int(days) >= 31:
        answer = input(
            "WARNING: Zulu date may have crossed into a new month. Does this date look correct? (type y or n) %s: " % (end_zulu))
        if answer == 'n':
            end_zulu = input("Please calculate the end date, the start date was " + str(
                start_zulu) + ' and you must add ' + str(added_time) + ' minutes. ')
    return(end_zulu)
