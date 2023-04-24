
from abstracts import Parameter, ParameterSet, units, NaN





class Barge(ParameterSet):
    Length:Parameter = 100 * units.meter
    Width:Parameter = 50* units.meter
    Depth:Parameter = 50* units.meter
    PlateThickness:Parameter = 12 * units.millimeter
    SteelDensity:Parameter = 7.850 * units.tonne/units.meter**3
    CoatingDensity:Parameter = 1.5 * units.gram/units.centimeter**2
    CoatingThickness:Parameter = 7 * units.millimeter


class VesselOutput(ParameterSet):
    Volume:Parameter = NaN * units.meter**3
    MassShell:Parameter = NaN * units.tonne
    MassCoating:Parameter = NaN * units.tonne
    MassTotal:Parameter = NaN * units.tonne
    Draft:Parameter = NaN * units.meter
    VolumeShell:Parameter = NaN * units.meter**3
    SurfaceOuterShell:Parameter = NaN * units.meter**2
    
    



barge = Barge()
barge.Length['inch'] = 4000
df = barge.to_dataframe()


def process(barge:Barge):
    output = VesselOutput()
    
    l = barge.Length['m']
    w = barge.Width['m']
    d = barge.Depth['m']



    output.Volume['m**3'] = volume = barge.Depth['m']*barge.Length['m']*barge.Width['m']
    t = barge.PlateThickness['m']
    inner_volume = (barge.Depth['m']-t)*(barge.Length['m']-t)*(barge.Width['m']-t) - 8*t**2
    shell_volume = volume-inner_volume
    output.MassShell['tonne'] = shell_volume * barge.SteelDensity['tonne/m**3']
    
    shell_surface = l*w*2 + w*d*2 + d*l*2
    
    output.MassCoating['tonne'] = (shell_surface * barge.CoatingThickness['m']) * barge.CoatingDensity['tonne/m**2']
    return output



output = process(barge)
print(output.MassCoating['tonne'])
    
