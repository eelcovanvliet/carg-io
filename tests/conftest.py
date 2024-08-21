"""
    Dummy conftest.py for carg_io.

    If you don't know what this is for, just leave it empty.
    Read more about conftest.py under:
    - https://docs.pytest.org/en/stable/fixture.html
    - https://docs.pytest.org/en/stable/writing_plugins.html
"""

import pytest
from carg_io.abstracts import Parameter, ParameterSet, units, NaN

class Box(ParameterSet):
    Length:Parameter = 1 * units.meter
    Width:Parameter = 1* units.meter
    Height:Parameter = 1* units.meter