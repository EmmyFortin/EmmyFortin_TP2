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

        # Création du push button qui va call la fonction qui applique les changements à l'outliner
        self.organise_outliner_button = QPushButton("Organise Outliner")

        # Appelle la fonction organise_outliner
        self.organise_outliner_button.clicked.connect(self.organise_outliner)

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

            # Retourne les données chargées pour pouvoir les récupérées dans les fonctions qui compare le json et les objets maya
            return data

        except Exception as error:
            print(f"Could not load data from {json_file}")
            print(error)

    # def get objects : fonction qui récupère les objets sélectionner dans maya si la checkbox selected only est coché sinon on récupere tout
    def get_objects(self):

        # Si la case selected only est coché
        if self.selection_only_checkbox.isChecked():
            # ls retourne les noms (et les noms des types) d'objets qui sont dans la scène
            # je ne veux pas avoir les options qui sont dans le haut du outliner (display, show, help)
            # type = transform car transform représente de façon général les geo, lights, group, particules, cam etc.
            # je met la séléction à true ici pour juste renvoyé les objets selectionné (car checkbox selected only est coché)
            objects = cmds.ls(type="transform", selection = True)
        
        # Sinon on retourne tout les objets du outliner    
        else:
            objects = cmds.ls(type = "transform")
            
        return objects


    # Fonction qui permet d'appliquer la couleur aux objets dans l'outliner
    def apply_colors(self, data, objects):
        # Parcout les objets dans maya
        for object_name in objects:

            # On parcourt les items (paire = key et sa valeur) du JSON
            # On récupère le nom de la key et sa valeur (la couleur)
            for key_name, color in data.items():

                # Si les noms des keys du json correspondent aux noms des objets
                if key_name in object_name:

                    # On enable useOutlinerColor dans le attribut editor
                    cmds.setAttr(object_name + ".useOutlinerColor", True)

                    # On applique la couleur 
                    # le nom de l'attribut est .outlinerColor
                    # Color contient la valeur de la couleur correspondant au key_name 
                    # La couleur est une liste de 3 valeurs (RGB)
                    # on doit spécifie l'index pour avoir la couleur visuellement 

                    cmds.setAttr(
                        object_name + ".outlinerColor",
                        color[0],
                        color[1],
                        color[2]
                    )
                    break

    # Fonction qui permet d'appliquer l'ordre alaphabetique aux objets dans l'outliner
           
    def apply_reorder(self, data, objects):
        
        # Création d'une liste vide pour contenir les objets à reorder
        objects_to_reorder = []

        # Parcout les objets dans maya
        for object_name in objects:

            # Parcourt les noms des keys dans le fichier JSON
            for key_name in data:

                # Si le nom de la key présentement parcourut est dans le nom de l'objet présentement parcouru
                if key_name in object_name:

                    # On ajoute le nom de l'objet dans la liste d'objets à reorder
                    objects_to_reorder.append(object_name)
                    # Correspondance trouvé pour cet objet on arrête de chercher dans les autres key_name
                    break

        # Quand get_objects me renvoit la liste sans la séléction à true les objets sont déjà en ordre alphabetique 
        # Mais quand get_objects me renvoit la liste avec la sélection à true les objets ne sont pas en ordre alphabetique

        # Donc je dois réellement sort avant de reorder
        # sorted_objects est la liste des objets à reorder en ordre alphabetique
        sorted_objects = cmds.sortStringArray(
            objects_to_reorder,
            sortOrder="alphabetic"
        )
            
        # Parcourt tout les objets dans la liste d'objets à reorder en orde alphabetique
        for object_name in sorted_objects:

            # Reorder les objets en ordre alphabetique mais avec sélection les places dans le bas de la liste
            cmds.reorder(object_name, back=True)
                    
       
    # Fonction qui appelle tout (get_objects) et qui vérifie comment les checkbox sont :
    def organise_outliner(self):

        cmds.undoInfo(openChunk=True)

        # Protection si le programme plante. Il faut fermer le undoInfo car s'il reste ouvert et que sa plante ça peut causer des problèmes
        try :
            # La fonction load_json est appellée
            # Création d'une variable locale pour stocker les objets du fichier JSON retournés par load_json
            data = self.load_json()

            # La fonction get_objects est appellée
            # Création d'une variable locale pour stocker les objets retournés par get_objects
            objects = self.get_objects()

            # Pour vérifier l'état des checkbox (color et reorder seulement)
            # Si les deux checkbox sont cochés les deux vont s'appliquer
            # si color est checked on applique la color sur les éléments sélectionnés
            if self.apply_colors_checkbox.isChecked():
                self.apply_colors(data, objects)

            # si ordre est checked on applique l'ordre sur les éléments sélectionnés
            if self.apply_reorder_checkbox.isChecked():   
                self.apply_reorder(data, objects)

        # À la fin peut importe ce qu'il arrive on ferme le closeChunk
        finally:
            cmds.undoInfo(closeChunk=True)

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


