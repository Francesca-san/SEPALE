import os
import matplotlib.pyplot as plt
import numpy as np
from classroom import *
#from student import *

# The first number refers to the abscissa 
# the second to the ordinate
plt.rcParams["figure.figsize"] = (25,5)
plt.rcParams["font.size"] = 7

# We define a new class called "All_classrooms"
class All_classrooms(Classroom):
    '''
    This is a description of the class, 
    If you have any problem with it
    you can always write help(All_classrooms)
    '''
    # This is the initializing function of any exercise
    # It has only one argument, called "base"
    def __init__(self, base_list):
        # Here we define the shared attributes of all the students
        # They all have a path, the base of the directory
        self.base_list = base_list
        #self.find_log_dir()
        # A classroom contains several students
        self.student_list = []
        list_classpath = os.listdir(self.base_list)
        for class_path in list_classpath:
            # PATH WARNING !!!!!!!!!!!!!!!!
            classe = Classroom(base_list + class_path)
            
            self.student_list.extend(classe.student_list)
        #student_list = os.listdir(self.base_list)
        #print(self.student_list)
        
