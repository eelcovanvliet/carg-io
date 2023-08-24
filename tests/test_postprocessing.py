import pytest
from pathlib import Path
from carg_io.abstracts import Parameter, ParameterSet, units, NaN
from carg_io.implementations import MyContainer, Box, BoxResults
from carg_io.postprocessing import Analyze
from random import randint

__author__ = "eelco van Vliet"
__copyright__ = "eelco van Vliet"
__license__ = "MIT"


TEMP = Path(__file__).parent / 'temp'
TEMP.mkdir(exist_ok=True)


def test_post_process():
    

    class BoxI(ParameterSet):
        Length:Parameter = 1 * units.meter
        Width:Parameter = 1* units.meter
        Height:Parameter = 1* units.meter

    class BoxO(ParameterSet):
        Mass:Parameter = 1 * units.meter
        Volume:Parameter = 1* units.meter
        
    def create_io():
        boxi = BoxI()
        for parameter in boxi:
            unit = parameter._unit_default
            parameter[unit] = randint(0,10)
        
        boxo = BoxO()
        for parameter in boxo:
            unit = parameter._unit_default
            parameter[unit] = randint(0,10)
        return [boxi, boxo]
    
    aaa = [create_io() for ix in range(10)]

    aaa = Analyze(aaa)
    aaa.get_double_scatter(show=True)












