import pytest
from carg_io.abstracts import Parameter, ParameterSet, units, NaN
from conftest import Box, block
from carg_io.abstracts import SettingAttributeNotAllowed




def test_parameter1():
    
    height = Parameter('height', 8*units.meter)
    assert height.is_default
    assert height.name == 'height'
    assert height['mm'] == 8000


def test_parameter_set():

    box = Box()
    assert box.Length['km'] == 1e-3

    
# def test_hash():
#     box = Box()
#     box.Height['m'] = 99
#     identical_box = Box()
    
#     identical_box.Height['mm'] = 99_000
#     hash1 = hash(box)
#     hash2 = hash(identical_box)
#     assert hash1 == hash2 # the hash checks if the instance values are equal
#     assert box != identical_box # the instances themselves are not equal

def test_pickle():
    box = Box()
    file = box.to_pickle()

def test_parm_equality1():
    box1 = Box()
    box2 = Box()
    assert box1.Length == box2.Length

def test_parm_equality2():
    box1 = Box()
    box2 = Box()
    box1.Length["cm"] == box1.Length["m"]/100
    assert box1.Length == box2.Length

def test_set_equality():
    box1 = Box()
    box2 = Box()
    assert box1 == box2

def test_set_not_equality():
    box1 = Box()
    box2 = Box()
    box2.Length["m"] = 123
    assert not box1 == box2

def test_setting_parm_error():
    box1 = Box()
    with pytest.raises(SettingAttributeNotAllowed):
        box1.Length = 123

def test_dependent_parm(block):
    assert block.Mass["pounds"]

def test_default_value(block):
    """Test that setting a value changes the 'is_default' attribute
    from True to False."""
    assert block.Length.is_default
    block.Length["m"] = block.Length["m"] + 1
    assert not block.Length.is_default

def test_repr(block):
    assert block.__repr__() == "ParameterSet(name='Block')"


