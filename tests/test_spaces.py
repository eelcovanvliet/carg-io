import pytest
from carg_io.abstracts import Parameter, ParameterSet, units, NaN
from carg_io.spaces import Space
from conftest import block_space
import numpy as np

__author__ = "eelco van Vliet"
__copyright__ = "eelco van Vliet"
__license__ = "MIT"


def test_space(block_space):
    assert len(block_space) == 10**3

def test_criteria(block_space):
    block_space.add_criteria("Volume", 'm**3', lambda v: v < 10*10*9)
    # There should be four cases that will not pass this criteria:
    # everything 10 m, or any combination of two parameters being 10 m.
    # = 4 cases
    assert len(block_space) == 10**3-4
    


