

Ir. E. van Vliet

24-07-2023

# Carg-io

`carg-io` supports defining, setting and bookkeeping when working with sets of parameters.
`carg-io` originated as an alternative to using the python-native `dataclass`, since `dataclasses` did not really offer the functionality needed for parametric analyses.

## Features

- Unit conversion
- Assigning default values
- Linting and autocompletion
- Hashing
- Iteration
- Representations for `pandas.dataframe` and `tkinter`


## Basic use:

### Creating Parameters
Below an example of how to organize the parameters for a box object.


```python
from carg_io import ParameterSet, Parameter, units

class Box(ParameterSet):
    Length:Parameter = 1 * units.meter
    Width:Parameter = 1 * units.meter
    Height:Parameter = 1 * units.meter
    Density:Parameter = 2 * units.kilogram / units.meter**3


if __name__ == "__main__":
    box = Box()
    box.Length['m'] = 2
    assert box.Length['mm'] == 2000

```
### Setting/getting parameters

When setting or getting parameters you *always* define a unit.


```
box.Width["m"] = 4
print(f"Box is {box.Width["foot"]} foot wide")

```

When creating a `Box`, it is always created with default values.
You can then change these parameters to what you want them to be.



### Creating dependent parameters
Your normal parameters are *independent*, i.e. they are at the core of what defines a `Box`.
In the example below, `Box.Volume` is a *dependent* parameter, in that it is fully defined by the length, width and height of the box.

```python
from carg_io import ParameterSet, Parameter, units

class Box(ParameterSet):
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
    box = Box()
    box.Length['m'] = 2
    assert box.Mass['t'] == 2000

```

## No categorical data
Categorical data, such as as choice between `GREEN`, `BLUE`, `YELLOW`, is deliberately not supported.
The reason for this is that `carg-io` focusses on numerical values only, since only numerical values can be shown in a graph.

Typically, digging deeper into categorical values, one will eventually find numerical values again. E.g. the colors `GREEN`, `BLUE` and `YELLOW` are actually wave lenghts 550, 450 and 580 nm.


