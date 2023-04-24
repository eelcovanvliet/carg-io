from __future__ import annotations
from carg_io.abstracts import Parameter, ParameterSet, units, NaN
from carg_io.cargo import Container
import zipfile


"""
Here are some example implementations of the abstracts and cargo

"""





class Box(ParameterSet):
    Length:Parameter = 1 * units.meter
    Width:Parameter = 1* units.meter
    Height:Parameter = 1* units.meter
    Density:Parameter = 2 * units.kilogram / units.meter**3

class BoxResults(ParameterSet):
    Volume:Parameter = NaN * units.meter**3
    Mass:Parameter = NaN * units.kilogram



class MyContainer(Container):
    i = [Box]
    o = [BoxResults]

    @staticmethod
    def load(file:str) -> MyContainer:
        inst = Container.load(file, MyContainer) #TODO: is there a way to put this entire method in the super somehow?
        return inst

