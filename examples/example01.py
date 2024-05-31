from carg_io.abstracts import Parameter, ParameterSet, units, NaN
from carg_io.spaces import Space
from carg_io.postprocessing import Analyze
import numpy as np


class IBeam(ParameterSet):
    Height:Parameter = 0.3 * units.m
    Width:Parameter = 0.2 * units.m
    Length:Parameter = 10 * units.m
    ThicknessWeb:Parameter = 10 * units.mm
    ThicknessFlange:Parameter = 10 * units.mm
    E:Parameter = 210 * units.GPa
    Density:Parameter = 7850 * units.kg/units.m**3

class IBeamOutput(ParameterSet):
    Volume:Parameter = NaN * units.m**3
    Mass: Parameter = NaN * units.kg
    CrossSectionArea = NaN * units.m**2
    SurfaceArea = NaN * units.m**2
    Ixx: Parameter = NaN * units.m**4
    MaxDeflextionPerTonne = NaN * units.mm
    

def calculate(ibeam:IBeam) -> IBeamOutput:
    out = IBeamOutput()

    tw = ibeam.ThicknessWeb['m']
    tf = ibeam.ThicknessFlange['m']
    w = ibeam.Width['m']
    h = ibeam.Height['m']
    l = ibeam.Length['m']

    Aw = tw * h 
    Af = tf * h
    If = 1/12 * w * tf**3
    If += (Af * (h/2)**2)
    Iw = 1/12 * tw * h**3
    out.Ixx['m**4'] = I = Iw + 2*If

    out.CrossSectionArea['m**2'] = Atot = Aw + 2 * Af
    out.Volume['m**3'] = V = Atot * l
    out.Mass['kg'] = V * ibeam.Density['kg/m**3']
    out.MaxDeflextionPerTonne['m'] = 1000 * 9.81 * l / (48 * ibeam.E['Pa'] * I)
    out.SurfaceArea['m**2'] = w*l*4 + h*l*2 + Atot*2
    return out


space = Space(IBeam)

space.expand(IBeam.Length, 'm', np.linspace(5, 15, 4))
space.expand(IBeam.Height, 'm', np.linspace(0.1, 0.5, 4))
space.expand(IBeam.ThicknessFlange, 'mm', np.linspace(8, 30, 4))
space.expand(IBeam.ThicknessWeb, 'mm', np.linspace(8, 30, 4))

results = []
for i in space.construct():
    o = calculate(i)
    results.append((i,o))

analysis = Analyze(results)
analysis.get_double_scatter(show=True)




