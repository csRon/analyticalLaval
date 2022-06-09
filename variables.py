import numpy as np

def area_function(x):
    '''
    This method calculates the area of a given x-position A(x)
    @params: 	x Position can either be np.array or float
    @returns:	np.array or float area of the given position
    '''
    if x<5:
        return 1.75 - 0.75*np.cos((0.2*x-1)*np.pi)
    else:
        return 1.25 - 0.25*np.cos((0.2*x-1)*np.pi)


def init():
    global pi, po # input and output pressures
    global k  # isentropic coefficient
    global x  # x-position of the nozzle
    global po_pi_under  # ratio to reach transsonic speed
    global po_pi_over  # ratio to get shock inside the nozzle
    global Astar, A, vA  # nozzle areas
    global mach_under, mach_over  # mach distribution


    # initialization of input
    pi = 1
    po = 0.75
    k = 1.4

    # initialization of necessary variables
    x = np.linspace(0, 10, 200)
    Astar = 0
    vA = np.vectorize(area_function)  # vectorize so that its usable with np-array
    mach_under = np.zeros(len(x))
    mach_over = np.zeros(len(x))