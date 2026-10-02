import sys
import json

import maya.cmds as cmds
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QMessageBox,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QLabel,
    QLineEdit,
)


# 1 Création de l'interface du Outliner Organiser

# Class MainWindow qui va contenir l'interface de l'outil

class MainWindow(QMainWindow):


    def __init__(self):
        super().__init__()

        self.setWindowTitle("Outliner Organiser")

        # Appelle la fonction qui créer l'
        self.create_ui()

    def create_ui(self):

        # Création des widgets de l'interface utilisateur
        print("UI called")






# Fonction d'exécution principale de l'interface / app

def main(): 

    global app
    try:
        app.close()
    except Exception:
        pass
    # Création de l'application en passant en paramètres les arguments
    #app = QApplication(sys.argv)

    # Création de ma fenêtre principale et appel de son constructeur
    app = MainWindow()

    # Afficher la fenêtre principale car elle est caché par défaut
    app.show()

    # Boucle d'exécution de l'app
    #sys.exit(app.exec())


# Vérification de si le fichier est en standalone
#if __name__ == "__main__":
main()


