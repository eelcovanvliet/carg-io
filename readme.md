

Ir. E. van Vliet

24-07-2023

# Carg-io

`cargi-io` supports defining, setting and bookkeeping when working with sets of parameters.
`cargi-io` originated as an alternative to using the python-native `dataclass`, since `dataclasses` did not really offer the functionality needed for parametric analyses.

## Features

- Unit conversion
- Assigning default values
- Linting and autocompletion
- Hashing
- Iteration
- Representations for `pandas.dataframe` and `tkinter`


## Examples:

### Independent parameter
Below an example of how to organize the input parameters for a box object.

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

### Dependent parameter
In the example below, `Box.Volume` is a *dependent* parameter that uses the length, width and height of the box.

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
        return Parameter('Volume', l*w*h*units.meter**3)

```










### Unit conversion



## No categorical data
Categorical data, such as as choice between `GREEN`, `BLUE`, `YELLOW`, is deliberately not supported. 


## Terminology
Dependent versus independent variables

