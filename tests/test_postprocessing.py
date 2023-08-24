import pytest
from pathlib import Path
from carg_io.abstracts import Parameter, ParameterSet, units, NaN
from carg_io.implementations import MyContainer, Box, BoxResults
from carg_io.postprocessing import Analyze
from random import randint
import numpy as np
import itertools

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
        Mass:Parameter = 1 * units.kg
        Volume:Parameter = 1 * units.meter**3
        WeldLength:Parameter = 1 * units.meter
    


    def create_input_space():
        space = {
            "Length": np.linspace(2, 10, 10),
            "Width": np.linspace(2, 10, 10),
            "Height": np.linspace(2, 10, 10),
        }

        input = []
        for length, width, height in itertools.product(*space.values()):
            boxi = BoxI()
            boxi.Length['m'] = length
            boxi.Width['m'] = width
            boxi.Height['m'] = height
            input.append(boxi)
        return input

        
    def calculation(inputs):
        aaa = []
        for i in inputs:
            i:BoxI
            o = BoxO()
            l = i.Length['m']
            w = i.Width['m']
            h = i.Height['m']
            o.Volume['m**3'] = l * w * h
            o.WeldLength['m'] = 4 * (l + w + h)
            o.Mass['kg'] = l * w * h * 7850
            aaa.append([i, o])

        return aaa
    


    aaa = create_input_space()
    bbb = calculation(aaa)

    analysis = Analyze(bbb)
    analysis.get_double_scatter(show=True)












