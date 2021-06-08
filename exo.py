# On importe des petits modules python bien sympa
# numpy : fonctions mathématiques vraiment convenables !
import numpy as np


# On définit la classe Exo
class Exo:
    '''
    Ceci est la description de la classe
    Si tu as un problème avec cette classe
    tu peux taper help(Exo)
    '''
    # Ceci va être la fonction d'initialisation d'un exercice
    # son argument est path, le chemin du fichier
    def __init__(self, path):
        # Ici nous définissons les attributs communs à tous les exos
        self.path = path
        # Les keys numériques valables pour tous les exos
        self.numeric_keys = ['Response Time', 'NbErreurs', 'Repetitions']
        # Tout exo contient des lignes
        self.get_lines()
        self.clean_lines()
        self.parse_lines()
    
    def get_lines(self):
        f = open(self.path, 'r')
        # on récupère les lignes
        self.lines = f.readlines()
        # on ferme le fichier
        f.close()
    
    def clean_lines(self):
        # On enlève les \n pour tout le monde
        for i in range(len(self.lines)):
            self.lines[i] = self.lines[i].replace("\n", "")
        # Si la ligne est vide, on la supprime
        # On fait une liste contenant les indices
        # des lignes vides pour leur défoncer la 
        # tronche ensuite mouhahahahaha
        to_delete = []
        for i in range(len(self.lines)):
            if len(self.lines[i]) == 0:
                to_delete.append(i)
        # Défonçage dans 3, 2 ....
        for i in to_delete:
            del self.lines[i]   
        
    def parse_lines(self):
        attributs = []
        # On sépare les lignes selon les tabulations
        for l in self.lines:
            attributs.append(l.split('\t'))
        # On setup la date et les keys
        self.date = attributs[0]
        self.keys = np.array(attributs[1])
        
        data = attributs[2:-1]
        
        self.stats_total = attributs[-1]
        columns = []
        
        for j, k in enumerate(self.keys):
            if k in self.numeric_keys:
                columns.append(np.array([float(data[i][j]) for i in range(len(data))]))
            else:
                columns.append(np.array([data[i][j] for i in range(len(data))]))
        # On a bien contruit columns, c'est le notre maintenant !!
        self.columns = columns
        # Pour ne pas perdre ses clés !
        self.key_to_index = {}
        for i, k in enumerate(self.keys):
            self.key_to_index[k] = i
        
    def display(self):
        # on parcours les keys
        for i in range(self.keys.shape[0]):
            print(f'{self.keys[i]} {self.columns[i]}')

    
    def criteria_by_key(self, key, criteria, zeros=False):
        if key not in self.keys:
            raise Exception('key not in my keys !')
        if criteria not in self.keys:
            raise Exception('criteria not in my keys !')
            
        # on récupère l'indice de la key/colonne
        k_index = self.key_to_index[key]
        # on récupère l'indice du criteria/colonne
        c_index = self.key_to_index[criteria]
        # On récopère les colonnes
        key_column = self.columns[k_index]
        criteria_column = self.columns[c_index]
        
        dico = {}
        # Pour chaque key, on garde trace
        # de la valeur du critère et du nombre 
        # de fois ou l'on rencontre cette clé
        # pour chaque key, elle pointe
        # vers un tableau qui est une structure
        # assez pratique tavu si on veut rajouter
        # des éléments (par clé), au fur et à mesure
        # dico[key] -> [valeur_critère, compteur d'occurences]
        for i, k in enumerate(key_column):
            value = criteria_column[i]
            if k not in dico.keys():
                dico[k] = [value, 1]
            else:
                dico[k] = [dico[k][0] + value, dico[k][1] + 1]
        # On retourne notre dictionnaire
        return dico
    
    
        
# Nous définissons maintenant un type d'exercice particulier : les 2AFC
class AFC2(Exo):
    '''
    Ceci est la description de la classe
    Si tu as un problème avec cette classe
    tu peux taper help(AFC2)
    '''
    # Ceci est attribut spécifique à AFC2 qui répertorie
    # les keys qui contiennent des quantités numériques
    
    # Ceci va être la fonction d'initialisation d'un exercice
    # son argument est path, le chemin du fichier
    def __init__(self, path):
        # Ici nous définissons les attributs communs à tous les exos
        super().__init__(path)

        
# Nous définissons maintenant un type d'exercice particulier : les 5AFC
class AFC5(Exo):
    '''
    Ceci est la description de la classe
    Si tu as un problème avec cette classe
    tu peux taper help(AFC2)
    '''
    # Ceci va être la fonction d'initialisation d'un exercice
    # son argument est path, le chemin du fichier
    def __init__(self, path):
        # Ici nous définissons les attributs communs à tous les exos
        super().__init__(path)
     
    
