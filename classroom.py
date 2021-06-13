import os
import numpy as np
from student import Student
from utils import merge_list_dicos, average_dico
from graphs import plot_table

class Classroom:
    '''
    This is a description of the class, 
    If you have any problem with it
    you can always write help(Classroom)
    '''
    
    def __init__(self, base):
        self.base = base
        self.create_students()
        
            
    def create_students(self):
        if self.base[-1] != "/":
            self.base += "/"
        self.student_list = []
        list_students = os.listdir(self.base)
        for student_path in list_students:
            student = Student(self.base + student_path)
            self.student_list.append(student)
            
    def criteria_by_key(self, key, criteria):
        res = {}
        # For each exercise, we retrieve the dictionaries
        list_dicos = []
        for student in self.student_list:
            list_dicos.append(student.criteria_by_key(key, criteria))
        return merge_list_dicos(list_dicos)
    
    def print_names(self):
        for student in self.student_list:
            print(student.name, student.surname, f"({len(student.exos)} exercises)")
                
        

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
        