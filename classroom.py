import os
import numpy as np
from student import Student
from utils import merge_list_dicos, average_dico
from graphs import *

# We define a new class called "Classroom"
class Classroom:
    '''
    This is a description of the class, 
    If you have any problem with it
    you can always write help(Classroom)
    '''
    
    # This is the initializing function of any exercise
    # It has only one argument, called "path"
    def __init__(self, base):
        # Here we define the shared attributes of all the students
        # They all have a path, the base of the directory
        self.base = base
        # A classroom contains several students
        self.create_students()
        
    # As this function is in the __init__ function, 
    # it means that the function will start  
    # any time the class Classroom is called.        
    def create_students(self):
        # in order to avoid error message, we
        # ask the function to add a slash 
        # to the base if there is none.
        if self.base[-1] != "/":
            self.base += "/"
        # we create an empty list
        self.student_list = []
        # list_students corresponds 
        # to all the elements in base
        list_students = os.listdir(self.base)
        # for the path of a student in the list
        for student_path in list_students:
            # a student is an instance which belongs
            # to the class Student which has one attribute,
            # base (or path). The path is the base and
            # the path to the student's exercises.
            student = Student(self.base + student_path)
            self.student_list.append(student)
            
    def criteria_by_key(self, key, criteria):
        res = {}
        # For each exercise, we retrieve the dictionaries
        list_dicos = []
        # for a student in the list of students
        for student in self.student_list:
            # we add to the empty list the 
            # results of their criteria by key
            list_dicos.append(student.criteria_by_key(key, criteria))
        return merge_list_dicos(list_dicos)
    
    
    def print_names(self):
        # for a student in the list of students
        for student in self.student_list:
            # we show their name and surname
            print(student.name, student.surname, f"({len(student.exos)} exercises)")
                
    def with_errors(dico, key='Stimulus', at_least=1):
    # we create an empty list
    result = []
    # for the variables i and val
    # in the dictionary "NbErreurs"
    for i, val in enumerate(dico['NbErreurs']):
        # if the value is greater or equal
        # to the value of at_least
        if val >= at_least:
            # we add the value to the dictionary
            result.append(dico[key][i])
    # we return the result
    return result

    def plot_table_by_key(self, key, xscale=0.5, yscale=4):
        criterias = np.array(["Repetitions", "NbErreurs",  "Response Time"])
        row_values = []
        # At the beginning we don't know
        # the labels of the lines
        row_labels = None
        for criteria in criterias:
            dico = average_dico(self.criteria_by_key(key, criteria))
            # If we don't know the labels of the lines
            # at this round, the labels of the lines
            # are the ones we've just retrieved
            labels = np.array(list(dico.keys()))
            values = np.array(list(dico.values()))
            if row_labels is None:
                row_labels = labels
            # If we know them, we check that those that
            # we've just retrieved are the same
            else:
                for i in range(len(labels)):
                    if row_labels[i] != labels[i]:
                        # If they are not the same, a 
                        # message of error is raised
                        raise Exception("Uncompatible labels")
            # We add the lines of the table
            row_values.append(values)
        row_values = np.array(row_values)
        plot_table(row_labels, criterias, row_values.T, xscale=xscale, yscale=yscale)
        
    def hist_all_exos(self, key, criteria, title, xlabel, ylabel, xrotation=None, yrotation=None):
        dico = average_dico(self.criteria_by_key(key, criteria))
        labels = np.array(list(dico.keys()))
        values = np.array(list(dico.values()))
        #values = np.array(list(dico.values()))[:,0]
        # This line makes it possible to only
        # display the keys for which at least
        # one mistake has been done by the student
        sel_arr = values != 0
        if np.all(sel_arr == False):
            pass
        else:
            plot_hist(labels[sel_arr], values[sel_arr], title, xlabel, ylabel, xrotation=xrotation, yrotation=yrotation)

    def chart_all_exos(self, key, criteria, title):
        dico = average_dico(self.criteria_by_key(key, criteria))
        labels = np.array(list(dico.keys()))
        values = np.array(list(dico.values()))
        #values = np.array(list(dico.values()))[:,0]
        sel_arr = values != 0
        if np.all(sel_arr == False):
            pass
        else:
            plot_chart(labels[sel_arr], values[sel_arr], title)