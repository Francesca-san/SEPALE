# On importe des petits modules python bien sympa
# numpy : fonctions mathématiques vraiment convenables !
import numpy as np
import os
# taille des figures
from graphs import *
from exo import *
from utils import *


def get_files_directory(directory, pattern="AFC"):
    if directory[-1] != "/":
        directory += "/"
    return [directory + fichier for fichier in os.listdir(directory) if  pattern in fichier]

# On définit la classe Eleve
class Eleve:
    '''
    Ceci est la description de la classe
    Si tu as un problème avec cette classe
    tu peux taper help(Eleve)
    '''

    def __init__(self, base):
        # Dossier de base
        self.base = base
        # dossier contenant les logfiles
        self.find_log_dir()
        # Récupère nom et prénom
        self.get_name()
        #self.file = file 
        self.create_exos()
        
    def get_name(self):
        # Parse the base path to get the names
        tmp = self.base.split('/')[-2]
        fullname = tmp.split('_')[0]
        splitted_name = fullname.split(' ')
        # Si un seul nom de famille
        if len(splitted_name) == 2:
            name, surname = splitted_name
        else:
            name = splitted_name[0]
            surname = " ".join(e for e in splitted_name[1:])
        self.name = name
        self.surname = surname
        
    def create_exos(self):
        # On crée des tuples qui associent un pattern
        # dans un fichier à la classe d'Exo qui lui correspond
        # les élements de assos sont des couples (pattern, classe)
        assos = [("2AFC", AFC2),
                 ("5AFC", AFC5)]
        exos = []
        # Pour chaque pattern, classe dans la liste assos
        for pattern, cl in assos:
            # On récupère les paths des fichiers correspondant au pattern
            # dans le directory de l'élève
            path_list = get_files_directory(self.directory, pattern=pattern)
            # Pour chacun de ces paths de fichiers
            for exo_path in path_list:
                # On instancie la classe d'exercice qui va bien
                exo = cl(exo_path)
                # On ajoute cette instance à la liste d'exos
                exos.append(exo)
        # Une fois la liste d'exos mise en place
        # elle est attribuée à l'élève
        self.exos = exos
        
    def criteria_by_key(self, key, criteria):
        res = {}
        # Pour chaque exo, on récupère les dicos
        list_dicos = []
        for exo in self.exos:
            list_dicos.append(exo.criteria_by_key(key, criteria))
        return merge_list_dicos(list_dicos)
    
    def find_log_dir(self):
        if self.base[-1] != "/":
            self.base += "/"
        continue_exploring = True
        current_dir = self.base
        # Tant que l'on est pas au bout de l'exploration
        while continue_exploring:
            # On récupère l'arborescence sous le dossier
            extended_list = os.listdir(current_dir)
            # On regarde combien d'éléments sont dans l'arborescence
            # S'il y a un seul élément
            if len(extended_list) == 1 and os.path.isdir(current_dir + extended_list[0]):
                # On vérifie que c'est bien un dossier et on continue
                # On concatène le path du nouveau dossier avec
                # son dossier parent pour pouvoir continuer
                # l'exploration
                current_dir = current_dir + extended_list[0] + '/'
                continue_exploring = True  
            # S'il y a plusieurs éléments
            else:
                # On vérifie que tous sont bien des fichiers
                for element in extended_list:
                    if not os.path.isfile(current_dir + element):
                        # Sinon message d'erreur
                        raise Exception("Wait, this is not a file!")
                # Si c'est le cas, on s'arrète
                continue_exploring = False
        # Set up mon directory pour les logfiles bouyaa
        self.directory = current_dir
    
    def chart_all_exos(self, key, criteria, title):
        for exo in self.exos:
            dico = exo.criteria_by_key(key, criteria)
            labels = np.array(list(dico.keys()))
            values = np.array(list(dico.values()))[:,0]
            print(exo.path)

            plot_chart(labels, values, title)
            
    def hist_all_exos(self, key, criteria, title, xlabel, ylabel, xrotation=None, yrotation=None):
        for exo in self.exos:
            dico = exo.criteria_by_key(key, criteria)
            labels = np.array(list(dico.keys()))
            values = np.array(list(dico.values()))[:,0]
            print(exo.path)
            plot_hist(labels, values, title, xlabel, ylabel, xrotation=xrotation, yrotation=yrotation)
