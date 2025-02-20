# -*- coding: utf-8 -*-
"""
Created on Wed Feb 19 09:29:26 2025

@author: malco
"""

from math import pi, sqrt

class DataProcessing:
    def __init__(self, radius, length):
        self.radius = 1.5 # mm
        self.length = 4 # mm
        
        def torque_to_stress(self, torque):
            """ Converts torque array from motor into shear and normal stress arrays """
            shear_stress = (3.3*torque)/(2*pi*(self.radius)**3) # MPa, If shear stress and shear strain curve is wanted, pull from here
            normal_stress = shear_stress*sqrt(3) # MPa
            return normal_stress
            
        def speed_to_strain(self, rotation):
            """ Converts rotation array in fractions of a rotation to shear and normal strain """
            rotation_rads = rotation*2*pi # rads
            shear_strain = ((self.radius)*rotation_rads)/self/length
            normal_strain = shear_strain/sqrt(3)
            return normal_strain
        
        def time_to_strain_rate(self, max_strain, time, rotation):
            """ Converts time and total rotation into strain rate """
            rotation_rads = rotation*2*pi # rads
            
        def write_to_excel(self):
            ""
            
            
            
        