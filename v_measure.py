import numpy as np
from scipy.stats import linregress
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt

Rsun = 695508
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





def funct(x,s,i):
    return(s*x+i)

def cme_line_fit(ts,hs):
    popt,pcov = curve_fit(funct,ts,hs)
    s,i = popt[0],popt[1]
    x = np.linspace(min(ts),max(ts),10)
    plt.scatter(ts,hs)
    plt.plot(x,(s*x+i),'r')
    plt.title("Velocity (km/s): " +str(s*Rsun/60))
    plt.show()

ts,hs = line_fit_cme()
print(ts,hs)
cme_line_fit(ts,hs)
