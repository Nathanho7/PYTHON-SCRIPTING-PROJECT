

import json         
import os            
from datetime import date  # Pour avoir la date d'aujourd'hui automatiquement


#  CLASSE Footballeur — Représente UN footballeur
# Ici chaque objet Footballeur = un joueur avec ses stats.
class Footballeur:

    def __init__(self, nom, poste, buts, passes_d, matchs):
        # __init__ est appelé automatiquement quand on crée un objet 
        # "self" représente l'objet lui-même

        self.nom      = nom               # Ex: "Mbappé"
        self.poste    = poste             # Ex: "Attaquant"
        self.buts     = int(buts)         # On force le type entier 
        self.passes_d = int(passes_d)    
        self.matchs   = int(matchs)       

        # Pour que la date soit automatique    
        self.date     = str(date.today()) 

  
    #  Calcul du G/A pour UN joueur précis
    def total_individuel(self):
        # G/A = Goals + Assists
        return self.buts + self.passes_d 


    #  Convertir l'objet en dictionnaire (pour sauvegarde JSON)
    def to_dict(self):
        # JSON ne comprend pas les objets Python, il comprend les dictionnaires
        return {
            "nom":      self.nom,
            "poste":    self.poste,
            "buts":     self.buts,
            "passes_d": self.passes_d,
            "matchs":   self.matchs,
            "date":     self.date,
            "total_ga": self.total_individuel()  # On l'ajoute pour afficher le total G/A 
        }

    #  Recréer un objet Footballeur depuis un dictionnaire
    @classmethod
    def from_dict(cls, data):
        # @classmethod = méthode qu'on appelle sur la CLASSE, pas sur un objet
        # Elle sert à recréer un objet Footballeur depuis un dictionnaire (lu depuis JSON)
        # "cls" = la classe elle-même (comme "self" mais pour la classe)
        return cls(
            nom      = data["nom"],
            poste    = data["poste"],
            buts     = data["buts"],
            passes_d = data["passes_d"],
            matchs   = data["matchs"]
        )
        #Ici le but du data est de dire à python : "Va chercher dans le dictionnaire data la valeur qui est associée à l'étiquette 'nom'"

    def __str__(self):
        
        return f"{self.nom} | {self.poste:<15} | {self.buts} buts | {self.passes_d} passes décisives"
        # :<15 = aligne à gauche sur 15 caractères: Pour un affichage propre sur le terminal. 


#  CLASSE PerformanceManager — Gère la LISTE de tous les footballeurs
class PerformanceManager:

    #Ficher ou on sauvegarde les footballeurs . 
    FICHIER = "footballeurs.json" 

    def __init__(self):
        # La liste qui contient tous les objets Footballeur
        self.footballeurs = [] 

        # Après création du manager, on charge les données existantes
        self.charger()

    #  Ajouter un footballeur
    def ajouter(self, nom, poste, buts, passes_d, matchs):
        nouveau = Footballeur(nom, poste, buts, passes_d, matchs)
        self.footballeurs.append(nouveau) 
        self.sauvegarder()                  # On sauvegarde immédiatement 
        return nouveau

    #  Supprimer un footballeur par son index (position dans la liste)
    def supprimer(self, index):
        if 0 <= index < len(self.footballeurs):   # Vérifie que l'index est valide
            self.footballeurs.pop(index)           # pop() retire l'élément à cette position
            self.sauvegarder()
            return True
        return False   # Index invalide

   
    #  Calculs des statistiques globales
    def total_buts(self):
        # sum() additionne tous les buts de tous les joueurs
        # c'est équivalent à une boucle for qui additionne
        return sum(f.buts for f in self.footballeurs)

    def total_passes(self):
        # sum() additionne toutes les passes décisives de tous les joueurs
        return sum(f.passes_d for f in self.footballeurs)

    def total_ga(self):
        # G/A total = total buts + total passes décisives
        return self.total_buts() + self.total_passes() 


    #  Calcul  des buts PAR poste (pour le graphique) 
    def buts_par_poste(self):
        totaux = {}   # Dictionnaire : { "Attaquant": 55, "Milieu": 10, ... }

        for f in self.footballeurs: 
            if f.poste in totaux:
                totaux[f.poste] += f.buts   # On additionne si poste déjà présent
            else:
                totaux[f.poste] = f.buts    # On crée l'entrée si nouveau poste 

        return totaux

    #  Sauvegarder dans le fichier JSON
    def sauvegarder(self):
        # On convertit chaque Footballeur en dictionnaire avec to_dict()
        data = [f.to_dict() for f in self.footballeurs] 
      
        
        # On ouvre le fichier en écriture ("w") avec encodage UTF-8
        with open(self.FICHIER, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
            # indent=4 : rend le JSON lisible (indenté)
            # ensure_ascii=False : garde les accents
   
    #  Charger depuis le fichier JSON
    
    
    def charger(self):
        # Si le fichier n'existe pas encore, on ne fait rien
        if not os.path.exists(self.FICHIER):
            return

        try:
            # On ouvre le fichier en lecture ("r") avec encodage UTF-8
            with open(self.FICHIER, "r", encoding="utf-8") as f:
                data = json.load(f)   # Lit le JSON et le convertit en liste de dicts

            # On recrée les objets Footballeur depuis chaque dictionnaire
            self.footballeurs = [Footballeur.from_dict(d) for d in data]
        except:
            # Si le fichier est corrompu ou illisible, on repart de zéro
            self.footballeurs = []  