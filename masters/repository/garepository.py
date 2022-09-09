from fileinput import filename
from geneticalgorithm import geneticalgorithm as Ganew
import numpy as np
from shapely.geometry import LineString
import os
import os.path
from os import path
import time
import pandas as pd

varbound = np.array([[0,1]]*88)

class XFoilRepository:
    
    def __init__(self, maximum_thickness,
                minimum_thickness, maximum_camber,
                minimum_camber):
       

        self.maximum_allowable_thickness = maximum_thickness
        self.minimum_allowable_thickness = minimum_thickness
        self.maximum_allowable_camber = maximum_camber
        self.minimum_allowable_camber = minimum_camber
        self.bezier_control_point_parameter_check = 0
    
    def generate_Bezier_Curve(self, val_a, val_b, val_c, val_d, val_e, val_f, val_g, val_h, val_u):
        """
        Function to generate Bezier Curves using the provided constants - 8 constants for 7th Order
        """
        a = float(val_a)
        b = float(val_b)
        c = float(val_c)
        d = float(val_d)
        e = float(val_e)
        f = float(val_f)
        g = float(val_g)
        h = float(val_h)
        u = float(val_u)

        member0 = ((1.0-u)**7.0)*a
        member1 = ((1.0-u)**6.0)*(u**1)*b*7.0
        member2 = ((1.0-u)**5.0)*(u**2)*c*21.0
        member3 = ((1.0-u)**4.0)*(u**3)*d*35.0
        member4 = ((1.0-u)**3.0)*(u**4)*e*35.0
        member5 = ((1.0-u)**2.0)*(u**5)*f*21.0
        member6 = ((1.0-u)**1.0)*(u**6)*g*7.0
        member7 = ((1.0-u)**0.0)*(u**7)*h

        P = member0 + member1 + member2 + member3 + member4 + member5 + member6 + member7

        return P   
    
    def binary_to_decimal(self, specified_array, value_a, value_b):
        """
        Function to convert a specified array from binary values to decimal values
        """
        self.specified_array = specified_array
        power = value_b - value_a
        base = 2
        exponent = power
        summation = 0

        for i in range(value_a, (value_b + 1)):
            summation += ((self.specified_array[i])*(base**exponent))
            exponent -= 1
        return summation
        
    def convert_chromosome_to_control_points(self, individual):
        """
        Function to take an individual and extract the control_points
        """
        self.chromosome = individual
        self.control_points_array = np.random.randint(1, size=11) #11control points
        for i in range(len(self.control_points_array)):
            a = i*8
            b = (i*8)+7
            self.control_points_array[i] = self.binary_to_decimal(self.chromosome,a,b)
        
        return self.control_points_array
    
    def convert_control_points_to_coordinates_new_parameters(self, control_points_array):
        """
        Function to take a control points array and convert it to coordinates
        """
        Value = control_points_array

        # Upper Surface x Control Points
        Ux1 = 1.00
        Ux2 = 0.95
        Ux3 = 0.65
        Ux4 = 0.357
        Ux5 = 0.174
        Ux6 = 0.04
        Ux7 = 0.00011
        Ux8 = 0.00

        # Upper Surface y Control Points
        Uy1 = 0.000018
        Uy2 = Value[0]
        Uy3 = Value[1]
        Uy4 = Value[2]
        Uy5 = Value[3]
        Uy6 = Value[4]
        Uy7 = Value[5]
        Uy8 = Ux8

        # Lower Surface x Control Points
        Lx1 = 1
        Lx2 = 0.875
        Lx3 = 0.5
        Lx4 = 0.36
        Lx5 = 0.205
        Lx6 = 0.115
        Lx7 = -1.00*Ux7
        Lx8 = 0

        # Lower Surface y Control Points
        Ly1 = -1.00 *Uy1
        Ly2 = 0.25 * Value[6]
        Ly3 = 0.7 * Value[7]
        Ly4 = -1.00 * Value[8]
        Ly5 = Value[9]
        Ly6 = -1.00 * Value[10]
        Ly7 = -1.00 * Uy7
        Ly8 = Lx8
        
        if Ly7 != 0:
            if (Ly6/Ly7) < 0.6:
                self.bezier_control_point_parameter_check = 1
            else:
                self.bezier_control_point_parameter_check = 0
    
        elif Ly2 < Ly3:
            self.bezier_control_point_parameter_check = 1
        else:
            self.bezier_control_point_parameter_check = 0

        xU = []
        yU = []
        xL = []
        yL = []

        data = pd.DataFrame(columns=['UpperX','UpperY'])

        d = 0
        for i in np.arange(0,1.05,0.05):
            xU.append(self.generate_Bezier_Curve(Ux1, Ux2, Ux3, Ux4, Ux5, Ux6, Ux7, Ux8, float(i)))
            yU.append((self.generate_Bezier_Curve(Uy1, Uy2, Uy3, Uy4, Uy5, Uy6, Uy7, Uy8, float(i)))/1000)
            data = data.append({'UpperX': xU[d], 'UpperY': yU[d]}, ignore_index=True)
            d+=1

        e = 0
        for i in np.arange(1.0,-0.05,-0.05):
            xL.append(self.generate_Bezier_Curve(Lx1, Lx2, Lx3, Lx4, Lx5, Lx6, Lx7, Lx8, float(i)))
            yL.append((self.generate_Bezier_Curve(Ly1, Ly2, Ly3, Ly4, Ly5, Ly6, Ly7, Ly8, float(i)))/1000)
            data = data.append({'UpperX': xL[e], 'UpperY': yL[e]}, ignore_index=True)
            e+=1
            
        np.savetxt(r'ou.dat', data.values, fmt='%1.6f') # Opens and writes to ou.dat file in the current working directory 
#         np.savetxt(r'C:\Users\frede\Desktop\checkout\dfpoints.txt', data.values, fmt='%1.6f')
        return data

    def calculate_max_thickness_new(self, coordinates):
        """ 27/01/22
        Function to calculate the maximum airfoil thickness from a set of provided airfoil coordinates
        """
        self.coordinates = coordinates
        df = self.coordinates
        y = df['UpperY']
        x_coords_airfoil = df['UpperX']


        number_of_divisions = 1000

        thickness = np.full((number_of_divisions,2),0.0)

        for division_num in range(1,number_of_divisions):
            division = division_num/number_of_divisions
            x_coords_line = np.full((42),division)

            first_line = LineString(np.column_stack((x_coords_airfoil, y)))
            second_line = LineString(np.column_stack((x_coords_line, y)))
            intersection = first_line.intersection(second_line)

            midpoint = ((LineString(intersection).xy[1][1] - LineString(intersection).xy[1][0])/2) + LineString(intersection).xy[1][0]
            approximate_thickness = (LineString(intersection).xy[1][1] - LineString(intersection).xy[1][0])
            thickness[division_num-1][0] = division_num/number_of_divisions
            thickness[division_num-1][1] = approximate_thickness


        thickness_list = thickness.tolist()
        thickness_indexes = [item[0] for item in thickness_list]
        thickness_values = [item[1] for item in thickness_list]

        max_thickness = max(thickness_values)
        max_thickness_index = thickness_values.index(max_thickness)/number_of_divisions
        rounded_max_thickness = round(max_thickness,6)
        
        return rounded_max_thickness
    
    def calculate_max_camber(self, camber_coordinates):
        """ 27/01/22
        Function to calculate the maximum airfoil camber from a set of provided airfoil coordinates
        """
        self.camber_coords = camber_coordinates
        df = self.camber_coords

        y = df['UpperY']
        x_coords_airfoil = df['UpperX']


        number_of_divisions = 1000

        camber = np.full((number_of_divisions,2),0.0)

        for division_num in range(1,number_of_divisions):
            division = division_num/number_of_divisions
            x_coords_line = np.full((42),division)

            first_line = LineString(np.column_stack((x_coords_airfoil, y)))
            second_line = LineString(np.column_stack((x_coords_line, y)))
            intersection = first_line.intersection(second_line)

            midpoint = ((LineString(intersection).xy[1][1] - LineString(intersection).xy[1][0])/2) + LineString(intersection).xy[1][0]
            camber[division_num-1][0] = division_num/number_of_divisions
            camber[division_num-1][1] = midpoint

        camber_list = camber.tolist()
        x_values = [item[0] for item in camber_list]
        y_values = [item[1] for item in camber_list]
        x_values.remove(0.0)
        y_values.remove(0.0)

        max_camber = max(y_values)
        max_camber_index = y_values.index(max_camber)/number_of_divisions

        rounded_max_camber = round(max_camber,6)
        
        return rounded_max_camber
    
    def delete_results_file_new(self, outfile:str):
        """
        Function to delete the save_AOA_range.txt file
        """
        if path.exists(outfile):
            os.remove(outfile)

    def determine_individual_fitness_new_5AOA(self, outfile:str):
        """
        Function to calculate the varied AOA fitness of an individual's results stored in the save.txt file
        """
        fitness = 0
        if not path.exists(outfile):
            return fitness
        with open(outfile, "r") as f:
            contents =f.readlines()
            if len(contents) < 13:
                fitness = 0
            else: 
                text = [contents[c] for c in range(12,len(contents))]
                AOA_fitnesses = []

                CLmax = 0
                decimal_remainder = 0
                initial_fitness = 0

                for item in text:
                    x = item.split()
                    CL = float(x[1])
                    CD = float(x[2])
                    fitness_at_single_AOA = (CL+CD+(CL/CD))
                    AOA_fitnesses.append(fitness_at_single_AOA)

                initial_fitness = (sum(AOA_fitnesses))

        return fitness

    
    def evaluate_fitness_parameters(self, solution_coordinates, outfile:str):
        
        control_points = self.convert_chromosome_to_control_points(solution_coordinates)
        coordinates = self.convert_control_points_to_coordinates_new_parameters(control_points)
        solution_max_thickness = self.calculate_max_thickness_new(coordinates)
        solution_max_camber = self.calculate_max_camber(coordinates)
        
        print('Checking..')
        if (solution_max_thickness < self.minimum_allowable_thickness):
            print('Fitness Check Complete 6')
            fitness = 0

        elif(solution_max_thickness > self.maximum_allowable_thickness):
            print('Fitness Check Complete 5')
            fitness = 0

        # Camber Range Condition is checked here i.e. greater than min and less than max
        elif(solution_max_camber < self.minimum_allowable_camber):
            print('Fitness Check Complete 4')
            fitness = 0

        elif(solution_max_camber > self.maximum_allowable_camber):
            print('Fitness Check Complete 3')
            fitness = 0

        # Ly6 control point should not be greater than 0
        elif(self.bezier_control_point_parameter_check > 0):
            print('Fitness Check Complete 2')
            fitness = 0
            self.bezier_control_point_parameter_check = 0

        
        else:
           
            np.savetxt(r'coords.dat', coordinates.values, fmt='%1.6f')
            with open("coords.dat", "r") as dat_file:
                with open('af.txt', "w") as txt_file:
                    for row in dat_file:
                        txt_file.write(row)

            self.delete_results_file_new(outfile)
            time.sleep(2)

            os.startfile("run_script_new_5AOA.bat")
            time.sleep(15)
            self.kill_analysis()
            
            fitness = self.determine_individual_fitness_new_5AOA(outfile)
            
        return fitness

def fitness(X):
    xfoil = XFoilRepository(
        0.12,
        0.09,
        0.07,
        0.04
    )

    return xfoil.evaluate_fitness_parameters(X, 'outfile.txt')

# def fitness(X):
    
#     return np.sum(X**2)

class GeneticAlgorithmRepository(Ganew):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
    def run(self):
        super().run()
    
    