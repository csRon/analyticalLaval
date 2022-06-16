import variables

import numpy as np
from scipy import optimize
import matplotlib.pyplot as plt
import pandas as pd

def area_mach_relation(M):
    '''
    This exquation is the relation between the mach number and the area
    ratio. It need to be a function to solve it with newton scheme.
    @params: 	mach number
    @returns:	relation between mach number and area ratio
    '''
    Astar = variables.Astar
    A = variables.A
    k = variables.k
    return (Astar / A) - M / ((1 + ((k - 1) / (k + 1)) * (M ** 2 - 1)) ** ((k + 1) / (2 * (k - 1))))


def calc_mach_and_pressure_distribution(M1, pi, po):
    '''
    This method calculates the distribution with a given inlet- and
    outlet pressure and a mach number before the shock.
    @params:	mach number before shock, inlet pressure, outlet
                pressure
    @returns:	list of mach distribution and pressure distribution
    '''

    x = variables.x
    k = variables.k
    vA = variables.vA

    # set all non relevant of mach_over to 0
    variables.mach_over[0:100] = 0

    # find out mach number after shock with given mach number before
    min_dif = abs(M1 - variables.mach_over)

    # find out position and and area of shock
    xs = np.where(min_dif == np.amin(min_dif))[0]
    As = variables.vA(x[xs])

    # calculate mach number after shock
    M2 = ((1 + ((k - 1) * M1 ** 2) / 2) / (k * M1 ** 2 - (k - 1) / 2)) ** 0.5

    # calculate the hypothetical smallest area for the distribution
    # behind the shock
    variables.Astar = As * M2 / ((1 + ((k - 1) / (k + 1)) * (M2 ** 2 - 1)) ** ((k + 1) / (2 * (k - 1))))

    # create an equation for the distribution after the shock with a
    # hypothetical smallest area
    def eq_after_shock(M):
        return (variables.Astar / A) - M / ((1 + ((k - 1) / (k + 1)) * (M ** 2 - 1)) \
                                  ** ((k + 1) / (2 * (k - 1))))

    # find out mach distribution after shock
    mach_after_shock = np.zeros(len(x))
    i = 0
    for A in vA(x):
        try:
            mach_after_shock[i] = optimize.newton(eq_after_shock, 0)
        except:
            mach_after_shock[i] = np.nan
        i += 1

    # merge results together for full mach distribution
    mach = np.zeros(0)
    # mach dist for subsonic part
    mach = np.append(mach, variables.mach_under[0:100])
    # mach dist for part until shock
    mach = np.append(mach, variables.mach_over[100:int(xs)])
    # mach dist for part after shock
    mach = np.append(mach, mach_after_shock[int(xs):200])

    # calculate presssure after shock
    pt2 = ((1 + ((k - 1) / 2) * mach[-1] ** 2) ** (k / (k - 1))) * po
    p_after_shock = pt2 * ((1 + ((k - 1) / 2) * mach[int(xs):200] ** 2) \
                           ** (-k / (k - 1)))

    # find out pressure before shock
    pt1_p1 = (1 + ((k - 1) / 2) * M1 ** 2) ** (k / (k - 1))
    p1_p2 = (1 + k * M2 ** 2) / (1 + k * M1 ** 2)
    p2_pt2 = ((1 + ((k - 1) / 2) * M2 ** 2) ** (-k / (k - 1)))
    pt1 = pt1_p1 * p1_p2 * p2_pt2 * pt2
    p_before_shock = pt1 * ((1 + ((k - 1) / 2) * mach[0:int(xs)] ** 2) \
                            ** (-k / (k - 1)))

    # merge results together for full pressure distribution
    p = np.zeros(0)
    p = np.append(p, p_before_shock)
    p = np.append(p, p_after_shock)

    return [mach, p]


def guessing_method(pi: float, po: float,
                    max_error=0.0001, change_mach=0.001,
                    M1=1.6) -> tuple:
    '''
    This method wraps the guessing method to find the shock location.
    A guess of the mach number before the shock is taken by the user
    (default=1.6) and changed until the error is small enough (default=
    0.001
    @params: 	inlet pressure, outlet pressure, maximum difference
                between calculated pressure and inlet pressure pi,
                guessed mach number before shock
    @returns:	tuple of mach distribution and pressure distribution

    '''
    mach = np.zeros(0)
    p = np.zeros(0)
    error = np.inf
    first_run = True
    direction = ""
    while abs(error) > max_error:
        mach, p = calc_mach_and_pressure_distribution(M1, pi, po)
        pi_tot = pi - pi * (mach[0] ** 2) * 1.4 / 2
        error = pi_tot - p[0]
        direction_old = direction
        if error > 0:
            direction = '+'
            M1 += change_mach
        else:
            direction = '-'
            M1 -= change_mach
        if first_run:
            direction_old = direction
            first_run = False

        # check if the direction of the changed mach number changes (+
        # - + - ...) then it would be an infinite loop. The if case
        # avoids that.
        if direction_old != direction:
            return (mach, p)

    return (mach, p)


def find_shock(mach):
    '''
    This method finds the shock based on a hard criterion
    @params: 	mach number distribution
    @returns:	shocklocation
    '''
    for i in range(len(mach - 1)):
        diff = abs(mach[i] - mach[i + 1])
        if diff > 0.2:
            return variables.x[i]

def save_as_csv(mach, p):
    dataset = pd.DataFrame({'x':variables.x, 'mach':mach, 'p':p}, columns=['x', 'mach', 'p'])
    dataset.to_csv('results/mach_and_p_over_x.csv', index=False)

def plot_nozzle_area():
    # plot the area function to see what if it is correct
    plt.figure()
    plt.plot(variables.x, variables.vA(variables.x), c='black')
    plt.grid()
    plt.title("nozzle area function")
    plt.xlabel('x-position')
    plt.ylabel('nozzle Area')
    plt.savefig("results/nozzle_area_function.png", dpi=200)

def plot_mach_number_with_shock(mach):
    # plot the mach number
    plt.figure()
    plt.plot(variables.x, mach, label='subsonic', c='r')
    plt.xlabel('x-Position')
    plt.ylabel('mach number')
    plt.grid()
    plt.savefig("results/mach_number_with_shock.png", dpi=200)

def plot_pressure_with_shock(p):
    # plot the mach number
    plt.figure()
    plt.plot(variables.x, p, label='subsonic', c='g')
    plt.xlabel('x-Position')
    plt.ylabel('pressure')
    plt.grid()
    plt.savefig("results/pressure_with_shock.png", dpi=200)

