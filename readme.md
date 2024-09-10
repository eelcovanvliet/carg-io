# Carg-io

`carg-io` helps ease working with sets of parameters.
Any parametric analysis

## Features

- Defining them
- Support units
- Checking if a default value was changed
- Checking parameter set equality


- Visualizing input/output parameter sets
- Export and load from conventional formats (pandas DataFrame)
- Tkinter representation

- Defining dependent parameters


`carg-io` originated as an alternative to using the python-native `dataclass`, since `dataclasses` did not really offer the functionality needed for parametric analyses.

## Basic use

### Parameters and ParameterSet
Below an example of how to organize the parameters for a block object.


```python
from carg_io import ParameterSet, Parameter, units

class Block(ParameterSet):
    Length:Parameter = 1 * units.meter
    Width:Parameter = 1 * units.meter
    Height:Parameter = 1 * units.meter
    Density:Parameter = 2 * units.kilogram / units.meter**3
```

`Block` is a set of 4 Parameters with each a default value and a default unit.
While developing, most IDE will auto-complete the namespaces, allowing for faster development.

When making an instance of `Block`, it will always be created with default values.
Then can be changed at will after. When changing (=setting) a parameter, always specify the unit in square brackets:

```python
block = Block()
block.Length['m'] = 2
```

Similarly, getting the current value of a parameter *also* requires a unit:

```python
l = block.Length['foot']
print(f"Length in foot is: {l}")
```







### Creating dependent parameters
Your normal parameters are *independent*, i.e. they are at the core of what defines a `Block`.
In the example below, `Block.Volume` is a *dependent* parameter, in that it is fully defined by the length, width and height of the block.

```python
from carg_io import ParameterSet, Parameter, units

class Block(ParameterSet):
    Length:Parameter = 1 * units.meter
    Width:Parameter = 1 * units.meter
    Height:Parameter = 1 * units.meter
    Density:Parameter = 2 * units.kilogram / units.meter**3

    def Volume(self) -> Parameter:
        l = self.Length['m']
        w = self.Width['m']
        h = self.Height['m']
        return Parameter('Volume', l*w*h * units.meter**3)

    def Mass(self) -> Parameter:
        v = self.Volume['m**3']
        rho = self.Density['kg/m**3']
        
        return Parameter('Mass', v*rho * units.kg)

if __name__ == "__main__":
    block = Block()
    block.Length['m'] = 2
    assert block.Mass['t'] == 2000

```

## No categorical data
Categorical data, such as as choice between `GREEN`, `BLUE`, `YELLOW`, is deliberately not supported.
The reason for this is that `carg-io` focusses on numerical values only, since only numerical values can be shown in a graph.

Typically, digging deeper into categorical values, one will eventually find numerical values again. E.g. the colors `GREEN`, `BLUE` and `YELLOW` are actually wave lenghts 550, 450 and 580 nm.


