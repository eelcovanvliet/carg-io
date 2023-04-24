
from typing import List
from .abstracts import ParameterSet
import zipfile
from pathlib import Path

class Container:
    """
    A collection of i/o parameters and any result files.

    This is an object-oriented datastorage, and propably pretty slow.
    But for more intensive stuff, we might have a relational database equivalent

    """
    def __init__(self, input:List[ParameterSet], output=List[ParameterSet]):
        self.input = input
        self.output = output
        self.files = []
    
    
    def save(self, file:Path):
        with zipfile.ZipFile(file, mode="w") as archive:
            if isinstance(self.files, list):
                for filename in self.files:
                    archive.write(filename)
            
            for pset in self.input + self.output:
                filename = pset.to_pickle()
                archive.write(filename)
            



    def get_partial_hash(self):
        pass
    
    def __hash__(self):
        pass

    def open(self):
        pass


    

class Vessel:
    """
    A collection of containers

    """

    def __init__(self, containers:List[Container]):
        self.containers = containers

    

class Database:
    """
    
    """
    pass