import os
import numpy as np
from eleve import Eleve
from utils import merge_list_dicos, average_dico
from graphs import plot_table

class Classroom:
    '''
    Ceci est la description de la classe
    Si tu as un problème avec cette classe
    tu peux taper help(Classroom)
    '''
    
    def __init__(self, base):
        self.base = base
        self.create_eleves()
        
            
    def create_eleves(self):
        if self.base[-1] != "/":
            self.base += "/"
        self.eleve_list = []
        list_students = os.listdir(self.base)
        for student_path in list_students:
            eleve = Eleve(self.base + student_path)
            self.eleve_list.append(eleve)
            
    def criteria_by_key(self, key, criteria):
        res = {}
        # Pour chaque exo, on récupère les dicos
        list_dicos = []
        for eleve in self.eleve_list:
            list_dicos.append(eleve.criteria_by_key(key, criteria))
        return merge_list_dicos(list_dicos)
    
    def print_names(self):
        for eleve in self.eleve_list:
            print(eleve.name, eleve.surname, f"({len(eleve.exos)} exercices)")
            
            
    def plot_table_by_key(self, key, xscale=0.5, yscale=4):
        criterias = np.array(["Repetitions", "NbErreurs",  "Response Time"])
        row_values = []
        # Au début on ne connait pas les 
        # labels des lignes
        row_labels = None
        for criteria in criterias:
            dico = average_dico(self.criteria_by_key(key, criteria))
            # Si on ne connait pas les labels des lignes
            # à ce tour de boucle, les labels des lignes
            # sont ceux que l'on vient de récupérer (smart hein ?!)
            labels = np.array(list(dico.keys()))
            values = np.array(list(dico.values()))
            
            if row_labels is None:
                row_labels = labels
            # Si on les connait, on vérifie que ceux qu'on
            # vient de récupérer sont les mêmes 
            # sinon ça fout la merde et tout
            else:
                for i in range(len(labels)):
                    if row_labels[i] != labels[i]:
                        raise Exception("Uncompatible labels")
            # Coool on ajoute petit à petit
            # les lignes de notre tableau
            # tel un écureuil amassant des glands !
            row_values.append(values)
        # Vazy balance tout ça en tableau
        # numpy avec des flammes et tout !!!
        row_values = np.array(row_values)
        plot_table(row_labels, criterias, row_values.T, xscale=xscale, yscale=yscale)



