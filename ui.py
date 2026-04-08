# ============================================================
#  ui.py — L'interface graphique (tkinter)
# ============================================================
# Ce fichier construit toutes les fenêtres et boutons.
# Il utilise PerformanceManager (models.py) pour la logique.

import tkinter as tk                        # La lib graphique standard Python
from tkinter import ttk, messagebox        # ttk = widgets améliorés, messagebox = popups
import matplotlib.pyplot as plt            # Pour les graphiques
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg  # Intègre matplotlib dans tkinter

from models import PerformanceManager      # On importe notre logique


# ==============================================================
#  CLASSE App — La fenêtre principale
# ==============================================================

class App:

    # Liste fixe des postes disponibles
    POSTES = ["Attaquant", "Milieu", "Défenseur", "Gardien"]

    def __init__(self, root):
        # "root" = la fenêtre principale tkinter, créée dans main.py
        self.root = root
        self.root.title("⚽ Performance Tracker")
        self.root.geometry("900x600")       # Taille de la fenêtre
        self.root.configure(bg="#1e1e2e")   # Couleur de fond (dark mode)

        # On crée le manager qui gère toute la logique
        self.manager = PerformanceManager()

        # On construit les différentes parties de l'interface
        self._build_header()
        self._build_form()
        self._build_table()
        self._build_footer()

        # On affiche les données déjà sauvegardées au démarrage
        self.rafraichir_tableau()

    # ----------------------------------------------------------
    #  En-tête : titre de l'appli
    # ----------------------------------------------------------
    def _build_header(self):
        # Frame = un conteneur pour regrouper des widgets
        header = tk.Frame(self.root, bg="#313244", pady=10)
        header.pack(fill="x")   # fill="x" = s'étire sur toute la largeur

        tk.Label(
            header,
            text="⚽ Gestionnaire de Performances",
            font=("Helvetica", 20, "bold"),
            bg="#313244",
            fg="#cdd6f4"    # Couleur du texte
        ).pack()

    # ----------------------------------------------------------
    #  Formulaire : ajouter un footballeur
    # ----------------------------------------------------------
    def _build_form(self):
        form = tk.Frame(self.root, bg="#1e1e2e", pady=10)
        form.pack(fill="x", padx=20)

        # --- Ligne 1 : Nom + Buts + Passes + Matchs ---
        ligne1 = tk.Frame(form, bg="#1e1e2e")
        ligne1.pack(fill="x", pady=5)

        # Champ Nom
        tk.Label(ligne1, text="Nom", bg="#1e1e2e", fg="#cdd6f4").pack(side="left")
        self.entry_nom = tk.Entry(ligne1, width=15, bg="#313244", fg="white")
        self.entry_nom.pack(side="left", padx=5)

        # Champ Buts
        tk.Label(ligne1, text="Buts", bg="#1e1e2e", fg="#cdd6f4").pack(side="left", padx=5)
        self.entry_buts = tk.Entry(ligne1, width=5, bg="#313244", fg="white")
        self.entry_buts.pack(side="left", padx=5)

        # Champ Passes décisives
        tk.Label(ligne1, text="Passes D", bg="#1e1e2e", fg="#cdd6f4").pack(side="left", padx=5)
        self.entry_passes = tk.Entry(ligne1, width=5, bg="#313244", fg="white")
        self.entry_passes.pack(side="left", padx=5)

        # Champ Matchs
        tk.Label(ligne1, text="Matchs", bg="#1e1e2e", fg="#cdd6f4").pack(side="left", padx=5)
        self.entry_matchs = tk.Entry(ligne1, width=5, bg="#313244", fg="white")
        self.entry_matchs.pack(side="left", padx=5)

        # --- Ligne 2 : Poste + boutons ---
        ligne2 = tk.Frame(form, bg="#1e1e2e")
        ligne2.pack(fill="x", pady=5)

        # StringVar = variable tkinter qui stocke la valeur sélectionnée dans le menu
        self.var_poste = tk.StringVar(value=self.POSTES[0])

        # OptionMenu = menu déroulant des postes
        menu = tk.OptionMenu(ligne2, self.var_poste, *self.POSTES)
        # *self.POSTES = décompresse la liste en arguments séparés
        menu.config(bg="#313244", fg="white")
        menu.pack(side="left", padx=5)

        # Bouton Ajouter — appelle ajouter_footballeur() au clic
        tk.Button(ligne2, text="➕ Ajouter", command=self.ajouter_footballeur, bg="#a6e3a1").pack(side="left", padx=20)

        # Bouton Graphique — appelle afficher_graphique() au clic
        tk.Button(ligne2, text="📊 Graphique", command=self.afficher_graphique, bg="#89b4fa").pack(side="left")

    # ----------------------------------------------------------
    #  Tableau des footballeurs (Treeview)
    # ----------------------------------------------------------
    def _build_table(self):
        frame = tk.Frame(self.root, bg="#1e1e2e")
        frame.pack(fill="both", expand=True, padx=20, pady=10)
        # expand=True = le tableau grandit quand on redimensionne la fenêtre

        # Définition des colonnes — "total" = G/A calculé par joueur
        colonnes = ("date", "nom", "poste", "buts", "passes_d", "matchs", "total")
        self.tableau = ttk.Treeview(frame, columns=colonnes, show="headings")
        # show="headings" = cache la colonne vide par défaut

        # Définir les en-têtes de chaque colonne
        self.tableau.heading("date",     text="📅 Date")
        self.tableau.heading("nom",      text="👤 Nom")
        self.tableau.heading("poste",    text="🏅 Poste")
        self.tableau.heading("buts",     text="⚽ Buts")
        self.tableau.heading("passes_d", text="🎯 Passes D")
        self.tableau.heading("matchs",   text="🏟️ Matchs")
        self.tableau.heading("total",    text="📊 TOTAL G/A")

        # Largeur identique pour toutes les colonnes
        for col in colonnes:
            self.tableau.column(col, width=100, anchor="center")

        # Scrollbar verticale liée au tableau
        self.tableau.pack(side="left", fill="both", expand=True)
        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=self.tableau.yview)
        self.tableau.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

        # Bouton Supprimer en dessous du tableau
        tk.Button(
            self.root,
            text="🗑️ Supprimer",
            command=self.supprimer_footballeur,
            bg="#f38ba8"    # Rouge clair
        ).pack(pady=5)

    # ----------------------------------------------------------
    #  Footer : affiche le total global
    # ----------------------------------------------------------
    def _build_footer(self):
        # Label mis à jour à chaque ajout/suppression
        self.label_total = tk.Label(
            self.root,
            text="",
            font=("Helvetica", 13, "bold"),
            bg="#1e1e2e",
            fg="#f9e2af"    # Jaune doux
        )
        self.label_total.pack(pady=5)

    # ----------------------------------------------------------
    #  Action : Ajouter un footballeur (appelée par le bouton)
    # ----------------------------------------------------------
    def ajouter_footballeur(self):
        try:
            nom = self.entry_nom.get()   # .get() récupère la valeur du champ

            # On convertit directement en int — si l'utilisateur tape du texte,
            # le except attrape l'erreur et affiche un message
            buts, passes, matchs = (
                int(self.entry_buts.get()),
                int(self.entry_passes.get()),
                int(self.entry_matchs.get())
            )

            # Tout est valide : on ajoute via le manager
            self.manager.ajouter(nom, self.var_poste.get(), buts, passes, matchs)
            self.rafraichir_tableau()

        except:
            # Si une conversion échoue, on affiche une popup d'erreur
            messagebox.showerror("Erreur", "Vérifie les nombres !")

    # ----------------------------------------------------------
    #  Action : Supprimer la ligne sélectionnée
    # ----------------------------------------------------------
    def supprimer_footballeur(self):
        sel = self.tableau.selection()   # Retourne l'id tkinter de la ligne sélectionnée

        if sel:
            # On récupère la position (index) dans le tableau et on supprime
            self.manager.supprimer(self.tableau.index(sel[0]))
            self.rafraichir_tableau()

    # ----------------------------------------------------------
    #  Rafraîchir le tableau (après ajout ou suppression)
    # ----------------------------------------------------------
    def rafraichir_tableau(self):
        # On efface toutes les lignes actuelles du tableau
        for row in self.tableau.get_children():
            self.tableau.delete(row)

        # On réinsère tous les footballeurs du manager
        for f in self.manager.footballeurs:
            self.tableau.insert("", "end", values=(
                f.date, f.nom, f.poste, f.buts, f.passes_d, f.matchs,
                f.total_individuel()    # Calcule le G/A pour ce joueur
            ))
            # "" = parent (racine), "end" = à la fin de la liste

        # On met à jour le bandeau du bas avec les totaux globaux
        self.label_total.config(
            text=f"Total Global : {self.manager.total_buts()} buts | {self.manager.total_passes()} passes | {self.manager.total_ga()} G/A"
        )

    # ----------------------------------------------------------
    #  Afficher un graphique camembert par poste
    # ----------------------------------------------------------
    def afficher_graphique(self):
        totaux = self.manager.buts_par_poste()   # Dict { poste: total_buts }

        if not totaux:
            return   # Rien à afficher si aucun joueur

        # Toplevel = fenêtre secondaire (enfant de la principale)
        fen = tk.Toplevel(self.root)

        # Création du graphique matplotlib
        fig, ax = plt.subplots(figsize=(5, 4), facecolor="#1e1e2e")
        # fig = la figure entière, ax = le graphique dans la figure

        ax.pie(
            totaux.values(),        # Les buts (tailles des parts)
            labels=totaux.keys(),   # Les noms des postes
            autopct="%1.1f%%",      # Affiche le pourcentage sur chaque part
            textprops={'color': "w"}
        )

        # On intègre le graphique matplotlib dans la fenêtre tkinter
        FigureCanvasTkAgg(fig, master=fen).get_tk_widget().pack()
        # get_tk_widget() = récupère le widget tkinter contenant le graphique
