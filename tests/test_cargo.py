import pytest
from pathlib import Path
from carg_io.abstracts import Parameter, ParameterSet, units, NaN
from carg_io.implementations import MyContainer, Box, BoxResults



__author__ = "eelco van Vliet"
__copyright__ = "eelco van Vliet"
__license__ = "MIT"


TEMP = Path(__file__).parent / 'temp'
TEMP.mkdir(exist_ok=True)


def test_container_io():
    

    def calculation(box:Box) -> BoxResults:
        results = BoxResults()
        volume = box.Length['m'] * box.Width['m'] * box.Height['m']
        results.Volume['m**3'] = volume
        results.Mass['kg'] = volume * box.Density['kg/m**3']
        return results


    box = Box()
    box_results = calculation(box)
    
    
    cont = MyContainer([box], [box_results])
    cont.save(TEMP / 'aaa.cio')

    aaa = MyContainer.load(TEMP / 'aaa.cio')












