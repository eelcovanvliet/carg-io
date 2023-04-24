import sys
from abc import ABC, ABCMeta, abstractmethod
from typing import Set, Callable, List, Dict
import pandas as pd
import numpy as np
from copy import deepcopy
import tkinter as tk
import pint
from decimal import Decimal
units = ureg = pint.UnitRegistry()
NaN = np.nan

class MetaParameterSet(type):
    """
    This type ensures that init ParameterSet creates NEW instances of all
    input parameters.
    """
    def __new__(cls, clsname, bases, clsdict):
        
        if clsname=='ParameterSet': # Ignore the super
            return super().__new__(cls, clsname, bases, clsdict)
        
        # Allocate parameter container
        parameters = []

        # Extend with parameters from super (recursive by definition)
        for base in bases:
            if hasattr(base, '_parameters'):
                parameters.extend(base._parameters)

        # Extend with own parameters
        
        for name, val in clsdict.items():
            if not name.startswith('_'):
                clsdict[name] = Parameter(name, val) # Value->Parameter substitution
                parameters.append(name)
                
        clsdict['_parameters'] = parameters

        # Store ParameterSet name # NOTE: may be replaced with __qualname__
        clsdict['_name'] = clsname

        return super().__new__(cls, clsname, bases, clsdict)

class Parameter():
    """The Parameter class facilitates a lot of bookkeeping around a single value.
    
    It supports both input and output parameters.
    It uses Pint to support units and their conversion.

    - unit support
    - getting and setting values
    - default values
    - tkinter representation
    - 


    """#doctag[Parameter-user]
    """


    """#doctag[Parameter-dev]
    
    def __init__(self, name, value: pint.Quantity or float or int):
        """Create a Parameter instance with value.

        value: Either a pint.Quantity, int or float. If int or float, the value will be
                converted into a dimensionless pint.Quantity.

        """
        if not isinstance(value, pint.Quantity):
            try:
                float(value)
                value = pint.Quantity(value) # Make dimensionless
            except Exception as err:
                raise TypeError(f'Parameter expect a number-like value, got {value}')
        
        self.name = name
        self._value = value
        self._unit_default = value.u # default unit
        self.is_default = True

    @property
    def normalized_value(self) -> float|int:
        """The normalized value of a `Parameter` is the value represented in the default unit.
        Any resulting zero decimals (as result of a unit conversion) are dropper (normalized).
        """#doctag[normalized_value]
        value = self._value.m_as(self._unit_default)
        nvalue = Decimal(value).normalize()
        return nvalue

    def __getitem__(self, unit:str):
        """Get the value in the requested unit. For dimensionless units, use
        Parameter[None] or Parameter[:].
        """
        if unit == None or isinstance(unit, slice):
            return self._value.m
        return self._value.m_as(unit)

    def __setitem__(self, unit:str, value:float or int):
        self._value = ureg.Quantity(value, unit)
        self.is_default = False


    def _to_tk(self, root):
        """Return tkinter representation
        
        Input:
            tkinter container entity

        Returns:
            Label(name), Entry(value), Label(unit)

        """

        name_label = tk.Label(root, text=self.name, anchor="w", width=22)

        entry = tk.Entry(root, bd = 1, width=12)
        entry.insert(0, self._value.m)
        unit = str(self._value.u)
        if unit == 'dimensionless':
            unit = '-'
        unit_label = tk.Label(root, text=unit, anchor="w", width=17)
        return name_label, entry, unit_label

    def __repr__(self):
        return f"Parameter(name='{self.name}'', value={self._value})"


class SettingAttributeNotAllowed(Exception):
    pass


class ParameterSet(metaclass=MetaParameterSet):
    
    _name:str
    _parameters:list
    
    LOCK_SETATTR = False

    def __init__(self):
        
        # Make copies of the default parameter instances
        for parm_name in self._parameters:
            parm = getattr(self, parm_name)
            setattr(self, parm_name, deepcopy(parm))
        self.LOCK_SETATTR = True
            

    def to_dataframe(self):
        stack = []
        for parameter in self:
            p:pint.Quantity = parameter._value
            # value = p.m if p.m < 1 else round(p.m,2) # FIXME: does not work for arrays
            stack.append((parameter.name, p.m, str(p.u), parameter.is_default))
        df = pd.DataFrame(stack, columns='name value unit is_default'.split())
        return df

    def to_dict(self) -> Dict[str, Parameter]:
        return {parameter.name:parameter for parameter in self}

    def __iter__(self) -> Parameter:
        for parm_name in self._parameters:
            yield getattr(self, parm_name)

    def __setattr__(self, attr, value):
        if self.LOCK_SETATTR and attr in self._parameters:
            raise SettingAttributeNotAllowed(f'It is not allowed to set {self._name}.{attr} directly. Use {self._name}.{attr}[<unit>] = {value} instead')
        object.__setattr__(self, attr, value)

    def copy(self):
        return deepcopy(self)

    @property
    def name(self):
        return self._name
    
    def _to_tk(self, root):
        """Return as tk representation"""
        frame = tk.LabelFrame(root, text=self.name, width=100, font=('Helvetica 9 bold'))
        
        entries = {}
        for row, parameter in enumerate(self):
            parameter:Parameter
            label, entry, unit = parameter._to_tk(frame)
            label.grid(row=row, column=0, padx=(2,2), pady=(2,2))
            entry.grid(row=row, column=1, padx=(2,2), pady=(2,2))
            unit.grid(row=row, column=2, padx=(2,2), pady=(2,2))
            entries[parameter.name] = entry

        return frame, entries

    def __getitem__(self, name:str):
        dictionary = self.to_dict()
        return dictionary[name]

    def __hash__(self):
        """Per default, the hash of a SubDesign is a frozenset containing the string representation
        of the parameter names and their value.
        The unit is NOT included, hence the value should always be represented in the initial
        unit.
        """
        fz = []
        for name, parm in self.to_dict().items():
            fz.append(self._name + name + str(parm.normalized_value))
        return hash(frozenset(fz))

    def get_partial_hash(self, parameter_names:List[str]):
        if not isinstance(parameter_names, (set, list, tuple)):
            raise TypeError(f"'parameter_names' must be a list, set or tuple. Got {type(parameter_names)}")
        stack = []
        for name in parameter_names:
            parm = self[name]
            string = self._name + name + str(parm._value.m)
            stack.append(string)
        return hash(frozenset(stack))



    
    
    