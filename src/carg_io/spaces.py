


from .abstracts import ParameterSet, Parameter, units
import itertools
from typing import Iterable
import numpy as np

class Space:
    """Space facilitates constructing large parameter input spaces"""

    _expansions = []
    _criteria = []

    def __init__(self, parameter_set:ParameterSet) -> None:
        self.parameter_set = parameter_set

    def expand(self, parameter:str|Parameter, unit:str, space:Iterable[float|int]):
        if isinstance(parameter, Parameter):
            parameter = parameter.name
        self._expansions.append((parameter, unit, space))

    def construct(self):
        """Construct the space based on the expansions and criteria"""
        parameters = [exp[0] for exp in self._expansions]
        units = [exp[1] for exp in self._expansions]
        iterables = [exp[2] for exp in self._expansions]

        space = []
        for values in itertools.product(*iterables):
            ps = self.parameter_set()
            for parameter, unit, value in zip(parameters, units, values):
                getattr(ps, parameter)[unit] = value
            space.append(ps)

        filtered_space = []
        for crit, point in itertools.product(self._criteria, space):
            parameter, unit, criteria = crit
            value = getattr(point, parameter)[unit]
            if criteria(value):
                filtered_space.append(point)
        return filtered_space

    def __len__(self):
        return len(space)
    
        
    def __iter__(self):
        pass
        

    def evelope(self):
        """Get min and max values of the entire space"""
        raise NotImplementedError()

    def is_block_uniform(self):
        """Check whether the input space is block uniform, i.e. all Parameters are
        equally and uniformly represented. Block-uniform datasets are nice for data
        analysis because they are unbiased"""
        raise NotImplementedError()



if __name__ == "__main__":
    
    class Box(ParameterSet):
        Length:Parameter = 1 * units.meter
        Width:Parameter = 1* units.meter
        Height:Parameter = 1* units.meter

        @property
        def Volume(self) -> Parameter:
            l = self.Length['m']
            w = self.Width['m']
            h = self.Height['m']
            return Parameter('Volume', l*w*h*units.meter**3)

    
    space = Space(Box)
    space.expand(Box.Length, 'm', np.linspace(1,10,10))
    space.expand(Box.Width, 'm', np.linspace(1,10,10))
    space.expand(Box.Height, 'm', np.linspace(1,10,10))

    space._criteria.append(("Volume", 'm**3', lambda v: v < 6**3))

    aaa = space.construct()
    aaa=1