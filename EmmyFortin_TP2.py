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
    QCheckBox
)


#----------------------------------------- 1 Création de l'interface du Outliner Organiser

# Class MainWindow qui va contenir l'interface de l'outil

class MainWindow(QMainWindow):


    def __init__(self):
        super().__init__()

        self.setWindowTitle("Outliner Organiser")
        self.resize(300, 100)

        # Appelle la fonction qui créer l'interface
        self.create_ui()

    def create_ui(self):

        # Création des widgets de l'interface utilisateur
        print("UI called")

        # Création du Widget parent de la main window
        widget = QWidget()

        # Création du layout vertical
        # Donne le layout au widget parent
        layout = QVBoxLayout(widget)

        # layout pour champ et label uniquement
        layout_json_path = QVBoxLayout()

        # Création du label du champ pour entrer le path
        self.json_path_label = QLabel("Enter JSON rule path")

        # Création du champ pour entrer le path
        self.json_path_field = QLineEdit()

        # Ajouter les widgets au layout pour le json path
        layout_json_path.addWidget(self.json_path_label)
        layout_json_path.addWidget(self.json_path_field)

        # Quand on fait "ENTER" sur le clavier on appelle la fonction qui load le json
        self.json_path_field.returnPressed.connect(self.load_json)

        # Création des widgets checkbox 
        self.selection_only_checkbox = QCheckBox("Apply on selection only")
        self.apply_colors_checkbox = QCheckBox("Apply colors")
        self.apply_reorder_checkbox = QCheckBox("Apply reorder")

        # Layout pour les 3 checkbox
        layout_checkbox = QVBoxLayout()

        layout_checkbox.addWidget(self.selection_only_checkbox)
        layout_checkbox.addWidget(self.apply_colors_checkbox)
        layout_checkbox.addWidget(self.apply_reorder_checkbox)

        # Création du push button qui va call la fonction qui organise l'outliner
        self.organise_outliner_button = QPushButton("Organise Outliner")

        # Layout du Qpushbutton
        layout_button = QVBoxLayout()
        layout_button.addWidget(self.organise_outliner_button)

        # Ajouter les layouts au layout principal
        layout.addLayout(layout_json_path)
        layout.addLayout(layout_checkbox)
        layout.addLayout(layout_button)


        # Position le widget dans le centre de la main window
        self.setCentralWidget(widget)



    def load_json(self):

        # Récupère le texte entrer dans le champ de texte du chemin du fichier json
        # Il faut aussi dire d'ignorer les espaces supplémentaires et les ""
        json_file = self.json_path_field.text().strip().strip('"')

        try: 
            # Chargement des données du fichier .json entré dans le champ
            with open(json_file, "r", encoding="utf-8") as file:
                data = json.load(file)

            print(data)

        except Exception as error:
            print(f"Could not load data from {json_file}")
            print(error)



# fonction qui organise l'outliner 
    # si checkbox 


# Fonction d'exécution principale de l'interface / app

def main(): 

    global ui_window
    try:
        ui_window.close()
    except Exception:
        pass

    # Création de ma fenêtre principale et appel de son constructeur
    ui_window = MainWindow()

    # Afficher la fenêtre principale car elle est caché par défaut
    ui_window.show()


# Vérification de si le fichier est en standalone
if __name__ == "__main__":
    main()


