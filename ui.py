import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from models import PerformanceManager

class App:
    POSTES = ["Attaquant", "Milieu", "Défenseur", "Gardien"]

    def __init__(self, root):
        self.root = root
        self.root.title("⚽ Performance Tracker")
        self.root.geometry("900x600")
        self.root.configure(bg="#1e1e2e")

        self.manager = PerformanceManager()

        self._build_header()
        self._build_form()
        self._build_table()
        self._build_footer()

        self.rafraichir_tableau()

    def _build_header(self):
        header = tk.Frame(self.root, bg="#313244", pady=10)
        header.pack(fill="x")
        tk.Label(
            header,
            text="⚽ Gestionnaire de Performances",
            font=("Helvetica", 20, "bold"),
            bg="#313244",
            fg="#cdd6f4"
        ).pack()

    def _build_form(self):
        form = tk.Frame(self.root, bg="#1e1e2e", pady=10)
        form.pack(fill="x", padx=20)

        ligne1 = tk.Frame(form, bg="#1e1e2e")
        ligne1.pack(fill="x", pady=5)

        tk.Label(ligne1, text="Nom", bg="#1e1e2e", fg="#cdd6f4").pack(side="left")
        self.entry_nom = tk.Entry(ligne1, width=15, bg="#313244", fg="white")
        self.entry_nom.pack(side="left", padx=5)

        tk.Label(ligne1, text="Buts", bg="#1e1e2e", fg="#cdd6f4").pack(side="left", padx=5)
        self.entry_buts = tk.Entry(ligne1, width=5, bg="#313244", fg="white")
        self.entry_buts.pack(side="left", padx=5)

        tk.Label(ligne1, text="Passes D", bg="#1e1e2e", fg="#cdd6f4").pack(side="left", padx=5)
        self.entry_passes = tk.Entry(ligne1, width=5, bg="#313244", fg="white")
        self.entry_passes.pack(side="left", padx=5)

        tk.Label(ligne1, text="Matchs", bg="#1e1e2e", fg="#cdd6f4").pack(side="left", padx=5)
        self.entry_matchs = tk.Entry(ligne1, width=5, bg="#313244", fg="white")
        self.entry_matchs.pack(side="left", padx=5)

        ligne2 = tk.Frame(form, bg="#1e1e2e")
        ligne2.pack(fill="x", pady=5)

        self.var_poste = tk.StringVar(value=self.POSTES[0])
        menu = tk.OptionMenu(ligne2, self.var_poste, *self.POSTES)
        menu.config(bg="#313244", fg="white")
        menu.pack(side="left", padx=5)

        tk.Button(ligne2, text="➕ Ajouter", command=self.ajouter_footballeur, bg="#a6e3a1").pack(side="left", padx=20)
        tk.Button(ligne2, text="📊 Graphique", command=self.afficher_graphique, bg="#89b4fa").pack(side="left")

    def _build_table(self):
        frame = tk.Frame(self.root, bg="#1e1e2e")
        frame.pack(fill="both", expand=True, padx=20, pady=10)

        colonnes = ("date", "nom", "poste", "buts", "passes_d", "matchs", "total")
        self.tableau = ttk.Treeview(frame, columns=colonnes, show="headings")

        self.tableau.heading("date", text="📅 Date")
        self.tableau.heading("nom", text="👤 Nom")
        self.tableau.heading("poste", text="🏅 Poste")
        self.tableau.heading("buts", text="⚽ Buts")
        self.tableau.heading("passes_d", text="🎯 Passes D")
        self.tableau.heading("matchs", text="🏟️ Matchs")
        self.tableau.heading("total", text="📊 TOTAL G/A")

        for col in colonnes:
            self.tableau.column(col, width=100, anchor="center")

        self.tableau.pack(side="left", fill="both", expand=True)
        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=self.tableau.yview)
        self.tableau.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

        tk.Button(self.root, text="🗑️ Supprimer", command=self.supprimer_footballeur, bg="#f38ba8").pack(pady=5)

    def _build_footer(self):
        self.label_total = tk.Label(
            self.root,
            text="",
            font=("Helvetica", 13, "bold"),
            bg="#1e1e2e",
            fg="#f9e2af"
        )
        self.label_total.pack(pady=5)

    def ajouter_footballeur(self):
        try:
            nom = self.entry_nom.get()
            buts, passes, matchs = (
                int(self.entry_buts.get()),
                int(self.entry_passes.get()),
                int(self.entry_matchs.get())
            )

            self.manager.ajouter(nom, self.var_poste.get(), buts, passes, matchs)
            self.rafraichir_tableau()
        except ValueError:
            messagebox.showerror("Erreur", "Vérifie les nombres !")

    def supprimer_footballeur(self):
        sel = self.tableau.selection()
        if sel:
            self.manager.supprimer(self.tableau.index(sel[0]))
            self.rafraichir_tableau()

    def rafraichir_tableau(self):
        # Réinitialise et remplit le tableau avec les données du manager
        for row in self.tableau.get_children():
            self.tableau.delete(row)

        for f in self.manager.footballeurs:
            self.tableau.insert("", "end", values=(
                f.date, f.nom, f.poste, f.buts, f.passes_d, f.matchs,
                f.total_individuel()
            ))

        self.label_total.config(
            text=f"Total Global : {self.manager.total_buts()} buts | {self.manager.total_passes()} passes | {self.manager.total_ga()} G/A"
        )

    def afficher_graphique(self):
        totaux = self.manager.buts_par_poste()
        if not totaux:
            return

        fen = tk.Toplevel(self.root)
        fig, ax = plt.subplots(figsize=(5, 4), facecolor="#1e1e2e")

        ax.pie(
            totaux.values(),
            labels=totaux.keys(),
            autopct="%1.1f%%",
            textprops={'color': "w"}
        )

        # Intègre le graphique Matplotlib dans l'interface Tkinter
        FigureCanvasTkAgg(fig, master=fen).get_tk_widget().pack()
