

import tkinter as tk      # La lib graphique
from ui import App        # On importe notre classe App depuis ui.py


# Ce bloc s'exécute UNIQUEMENT si on lance ce fichier directement
# (pas si on l'importe depuis un autre fichier)
if __name__ == "__main__":

    root = tk.Tk()     # Crée la fenêtre principale tkinter
    app = App(root)    # Crée notre application en lui passant la fenêtre
    root.mainloop()    # Lance la boucle d'événements 
                       # Le programme tourne ici jusqu'à ce qu'on ferme la fenêtre
