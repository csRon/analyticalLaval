#!/usr/bin/python3
import variables
import functions

from scipy import optimize
import os

def main():
	variables.init()

	os.makedirs('results', exist_ok=True)

	functions.plot_nozzle_area()
	print("Input pressure:\t\t%f"%variables.pi)
	print("Output pressure:\t%f"%variables.po)

	pi = variables.pi
	po = variables.po
	k = variables.k


	# find out mach distribution for nozzle without shock
	variables.Astar = 1
	for i, variables.A in enumerate(variables.vA(variables.x)):
		variables.mach_under[i] = optimize.newton(functions.area_mach_relation, 0)
		variables.mach_over[i] = optimize.newton(functions.area_mach_relation, 2)
	functions.plot_mach_number_without_shock()

	# calculate upper and lower bounds of pressure ratio to reach 
	# transsonic speed
	po_pi_under = (1 + ((k-1)/2)*variables.mach_under[-1]**2)**(-k/(k-1))
	po_pi_over = (1 + ((k-1)/2)*variables.mach_over[-1]**2)**(-k/(k-1))
	print("Min pressure ratio po/pi for subsonic flow:\n\t%f"%po_pi_under)
	print("Max pressure ratio po/pi for flow with shock inside nozzle:\n\t%f"%po_pi_over)

	if po/pi > po_pi_under or po/pi < po_pi_over:
		print("There is no shock!")
	else:
		print("Start guessing loops to find shock location..")
		mach, p = functions.guessing_method(pi, po, 0.0001, 0.01)
		functions.plot_mach_number_with_shock(mach)
		functions.plot_pressure_with_shock(p)
		print("Finished guessing loops to find shock location..")
		shock_location = functions.find_shock(mach)
		print("Shock location:\t\t%s"%shock_location)
	
	
if __name__ == "__main__":
	main()
