import json          
import os            
from datetime import date

class Footballeur:
    def __init__(self, nom, poste, buts, passes_d, matchs):
        self.nom      = nom
        self.poste    = poste
        self.buts     = int(buts)
        self.passes_d = int(passes_d)
        self.matchs   = int(matchs)
        self.date     = str(date.today())

    def total_individuel(self):
        return self.buts + self.passes_d 

    # Convertit l'objet pour la sauvegarde JSON (format dictionnaire)
    def to_dict(self):
        return {
            "nom":      self.nom,
            "poste":    self.poste,
            "buts":     self.buts,
            "passes_d": self.passes_d,
            "matchs":   self.matchs,
            "date":     self.date,
            "total_ga": self.total_individuel()
        }

    # Recrée un objet Footballeur depuis les données JSON
    @classmethod
    def from_dict(cls, data):
        return cls(
            nom      = data["nom"],
            poste    = data["poste"],
            buts     = data["buts"],
            passes_d = data["passes_d"],
            matchs   = data["matchs"]
        )

    def __str__(self):
        return f"{self.nom} | {self.poste:<15} | {self.buts} buts | {self.passes_d} passes"


class PerformanceManager:
    FICHIER = "footballeurs.json" 

    def __init__(self):
        self.footballeurs = [] 
        self.charger()

    def ajouter(self, nom, poste, buts, passes_d, matchs):
        nouveau = Footballeur(nom, poste, buts, passes_d, matchs)
        self.footballeurs.append(nouveau) 
        self.sauvegarder()
        return nouveau

    def supprimer(self, index):
        if 0 <= index < len(self.footballeurs):
            self.footballeurs.pop(index)
            self.sauvegarder()
            return True
        return False

    def total_buts(self):
        return sum(f.buts for f in self.footballeurs)

    def total_passes(self):
        return sum(f.passes_d for f in self.footballeurs)

    def total_ga(self):
        return self.total_buts() + self.total_passes() 

    def buts_par_poste(self):
        totaux = {}
        for f in self.footballeurs: 
            if f.poste in totaux:
                totaux[f.poste] += f.buts
            else:
                totaux[f.poste] = f.buts
        return totaux

    def sauvegarder(self):
        # Sérialisation des objets en dictionnaires avant l'écriture
        data = [f.to_dict() for f in self.footballeurs] 
        with open(self.FICHIER, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
   
    def charger(self):
        if not os.path.exists(self.FICHIER):
            return

        try:
            with open(self.FICHIER, "r", encoding="utf-8") as f:
                data = json.load(f)
            # Désérialisation : transforme les dictionnaires en objets Footballeur
            self.footballeurs = [Footballeur.from_dict(d) for d in data]
        except:
            self.footballeurs = []
