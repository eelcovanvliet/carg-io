from __future__ import annotations
from carg_io.abstracts import Parameter, ParameterSet, ParameterSetCombination, units, NaN
from carg_io.cargo import Container
import itertools
import pandas as pd


"""
Here are some example implementations of the abstracts and cargo

"""

class Box(ParameterSet):
    Length:Parameter = 1 * units.meter
    Width:Parameter = 1* units.meter
    Height:Parameter = 1* units.meter

class Truck(ParameterSet):
    Height: Parameter = 4 * units.m
    Capactity:Parameter = 40 * units.kg
    Cost: Parameter = NaN * units.dimensionless/units.km
    
class Road(ParameterSet):
    MaxHeight:Parameter = 5 * units.m
    Length: Parameter = 100 * units.km




class Calculation:

    @property
    def trucks(self):
        """This calculation uses the ParameterSet to create categorical data, i.e. Truck A, B and C
        with set values"""
        stack = []
        for height, cap, cost in [(3, 40, 300), (3.5, 50, 450), (4, 60, 500)]:
            truck = Truck()
            truck.Height['m'] = height
            truck.Capactity['kg'] = cap
            truck.Cost['1/km'] = cost
            stack.append(truck)
        return stack

    @property
    def roads(self):
        """This calculation uses the ParameterSet to create categorical data, i.e. Road A, B and C
        with set values"""
        stack = []
        for height, length in [(3, 100), (4, 80), (5, 85)]:
            road = Road()
            road.MaxHeight['m'] = height
            road.Length['km'] = length
            stack.append(road)
        return stack
    
    def calculate(self, box:Box):

        h = box.Height['m']

        single_box_cost = area = 6*h**2
        single_box_revenue = h**3

        box_df = box.to_dataframe(include_set_name=True)

        stack = []
        for truck, road in itertools.product(self.trucks, self.roads):

            truck:Truck
            road:Road
            
            if road.MaxHeight['m'] < truck.Height['m']: continue
            
            truck_cost = truck.Cost['1/m'] * road.Length['km']
            n = truck.Capactity['kg'] // area
            box_cost = single_box_cost * n
            revenue = single_box_revenue * n * 10

            df1 = box_df.copy()
            df2 = truck.to_dataframe(include_set_name=True)
            df3 = road.to_dataframe(include_set_name=True)

            df = pd.concat([df1, df2, df3])
            df.set_index('name', inplace=True, drop=True)

            df.loc['number_of_boxes', 'value'] = n
            df.loc['truck_cost', 'value'] = truck_cost
            df.loc['box_cost', 'value'] = box_cost
            df.loc['revenue', 'value'] = revenue
            df.loc['profit/loss', 'value'] = revenue-truck_cost-box_cost


            stack.append(df.value)

            

        df = pd.concat(stack, axis=1).T
        



        return df


if __name__ == "__main__":
    
    calc = Calculation()


    box = Box()

    stack = []
    for h in [1,2,3]:
        box = Box()
        box.Height['m'] = h
        df = calc.calculate(box)
        stack.append(df)
    df = pd.concat(stack)
    df.sort_values('profit/loss', ascending=False, inplace=True)
    df.plot()