# analyticalLaval

*analyticalLaval* solves for the mach number and the pressure distribution inside a given laval nozzle / convergent divergent (CD) nozzle.
It takes the pressures at input and output, as well as a nozzle function as input, calculated mach number and pressure distributions and the shock location (if there is a shock)

## Requirements
- python3.6 or newer
- see requirements.txt for others
- basic understanding of nozzle physics


## Install
```
git clone https://github.com/csRon/analyticalLaval.git
cd analyticalLaval
pip install -r requirements.txt
```
Test you installation by running
```
python main.py
```

## Getting started
The input of the program is defined in ``variables.py``. The physics is defined by:
- nozzle area function ``area_function`` (should describe a A(x) of a CD nozzle)
  - x-range of the area ``x`` (only the area you want to calculate)
- input pressure ``pi``
- output pressure ``po`` (note that pi>po)
- heat capacity ratio ``k`` (usually 1.4 for air)

You can play around a little bit with these inputs. The results will be in ``results`` folder and should be pretty self-explaining by their names.





## Background
This code comes from an older university project where it was used to validate CFD-results.
To understand the derivation of the equations take a look at JoshTheEngineers awesome video (https://www.youtube.com/watch?v=b0wvwkKqoVw).
If you are really interested in the derivation I can also recommend some other resources to handle the physics of CD nozzles (Unfortunately some of them are in german). Here is a list:
- https://www.aere.iastate.edu/~huhui/teaching/2017-01Sx/AerE344/class-notes/AerE344-Lecture-10-Shock_Waves_De_Laval_Nozzle.pdf
- https://itv.rwth-aachen.de/fileadmin/LehreSeminar/Thermodynamik_II/WS16_Vorlesungen/Thermodynamik_II_Kap4_Teil2von4.pdf
- http://homepages.hs-bremen.de/~kortenfr/Aerodynamik/script/node57.html


## License
automizedDoE is licensed under the MIT license.
