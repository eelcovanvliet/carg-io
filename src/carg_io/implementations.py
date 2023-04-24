from carg_io.abstracts import Parameter, ParameterSet, units, NaN
from carg_io.cargo import Container
import zipfile
import tkinter as tk

"""
Here are some example implementations of the abstracts and cargo

"""





class Box(ParameterSet):
    Length:Parameter = 1 * units.meter
    Width:Parameter = 1* units.meter
    Height:Parameter = 1* units.meter
    Density:Parameter = 2 * units.kilogram / units.meter**3

class BoxResults(ParameterSet):
    Volume:Parameter = NaN * units.meter**3
    Mass:Parameter = NaN * units.kilogram

class MyContainer(Container):

    @staticmethod
    def load(file:str):
        with zipfile.ZipFile(file, mode="r") as archive:
            box_data = archive.read('Box.pickle')
            box_results_data = archive.read('BoxResults.pickle')
        box = Box.from_serial_pickle(box_data)
        box_results = BoxResults.from_serial_pickle(box_results_data)
        return MyContainer(input=[box], output=[box_results])

    
    def file_ui(self):
        
        root = tk.Tk()
        
        input_column = tk.LabelFrame(root, text='INPUT', font=('Helvetica 10 bold'))
        input_parm = tk.Frame(input_column, width=360, height=520)
        for inp in self.input:
            frame, entries = inp._to_tk(input_parm, state='disabled')
            frame.pack(padx=(10,10), pady=(10,10), side=tk.TOP)
        

        output_column = tk.LabelFrame(root, text='OUTPUT', font=('Helvetica 10 bold'))
        output_parm = tk.Frame(output_column, width=360, height=520)
        for inp in self.output:
            inp:ParameterSet
            frame, entries = inp._to_tk(output_parm, state='disabled')
            frame.pack(padx=(10,10), pady=(10,10), side=tk.TOP)
        
        input_parm.pack(side=tk.TOP)
        input_column.pack(side=tk.LEFT)
        output_parm.pack(side=tk.TOP)
        output_column.pack(side=tk.LEFT)
        

        root.mainloop()