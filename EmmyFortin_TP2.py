import json

import maya.cmds as cmds
from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QMessageBox,
    QVBoxLayout,
    QPushButton,
    QLabel,
    QLineEdit,
    QCheckBox,
)


class MainWindow(QMainWindow):
    """Interface du Outliner Organiser."""

    def __init__(self):
        """Initialise la fenêtre principale."""
        super().__init__()

        self.setWindowTitle("Outliner Organiser")
        self.resize(300, 100)

        # Appelle la fonction qui créer l'interface
        self.create_ui()

    def create_ui(self):
        """Crée les widgets et les layouts de l'interface."""
        # Création du Widget parent de la main window
        widget = QWidget()

        # Création du layout vertical
        # Donne le layout au widget parent
        layout = QVBoxLayout(widget)

        # Layout pour champ et label uniquement
        layout_json_path = QVBoxLayout()

        # Création du label du champ pour entrer le path
        self.json_path_label = QLabel("Enter JSON rule path")

        # Création du champ pour entrer le path
        self.json_path_field = QLineEdit()

        # Ajouter les widgets au layout pour le json path
        layout_json_path.addWidget(self.json_path_label)
        layout_json_path.addWidget(self.json_path_field)

        # Création des widgets checkbox
        self.selection_only_checkbox = QCheckBox("Apply on selection only")
        self.apply_colors_checkbox = QCheckBox("Apply colors")
        self.apply_reorder_checkbox = QCheckBox("Apply reorder")

        # Layout pour les 3 checkbox
        layout_checkbox = QVBoxLayout()

        layout_checkbox.addWidget(self.selection_only_checkbox)
        layout_checkbox.addWidget(self.apply_colors_checkbox)
        layout_checkbox.addWidget(self.apply_reorder_checkbox)

        # Bouton qui applique les changements à l'outliner
        self.organise_outliner_button = QPushButton("Organise Outliner")

        # Appelle la fonction organise_outliner
        self.organise_outliner_button.clicked.connect(self.organise_outliner)

        # Layout du QPushButton
        layout_button = QVBoxLayout()
        layout_button.addWidget(self.organise_outliner_button)

        # Ajouter les layouts au layout principal
        layout.addLayout(layout_json_path)
        layout.addLayout(layout_checkbox)
        layout.addLayout(layout_button)

        # Positionne le widget dans le centre de la main window
        self.setCentralWidget(widget)

    def load_json(self):
        """Charge le contenu du fichier JSON."""
        # Récupère le texte du chemin du fichier json
        # Ignorer les espaces supplémentaires et les ""
        json_file = self.json_path_field.text().strip().strip('"')

        try:
            # Chargement des données du fichier .json entré dans le champ
            with open(json_file, "r", encoding="utf-8") as file:
                data = json.load(file)

            # Retourne les données chargées afin de les récupérées
            # dans les fonctions qui compare le json et les objets maya
            return data

        # S'il y a une erreur on afin un QMessageBox
        except Exception as error:
            QMessageBox.critical(
                self,
                "Invalid JSON path",
                f"Could not load data from JSON file :\n"
                f"{json_file}\n\n{error}",
            )
            # On ne poursuit pas les opérations
            return None

    def get_objects(self):
        """Récupère tous les objets ou seulement ceux
        sélectionnés dans Maya.
        """
        # Si la case selected only est cochée
        if self.selection_only_checkbox.isChecked():
            # ls retourne les noms
            # (et les noms des types) des objets dans la scène
            # Je veux ne pas les options
            # qui sont dans le haut du outliner (display, show, help)
            # type = transform
            # Transform représente de façon général
            # les geo, lights, group, particules, cam etc.
            # selection = True
            # Il renvoit les objets selectionnés
            # (car checkbox selected only est coché)
            objects = cmds.ls(type="transform", selection=True)

        # Sinon on retourne tout les objets du outliner
        else:
            objects = cmds.ls(type="transform")

        return objects

    def apply_colors(self, data, objects):
        """Applique la couleur aux objets dans l'outliner selon le JSON."""
        # Parcout les objets dans maya
        for object_name in objects:

            # On parcourt les items (paire = key et sa valeur) du JSON
            # On récupère le nom de la key et sa valeur (la couleur)
            for key_name, color in data.items():

                # Si les noms des keys du json correspondent
                # aux noms des objets
                if key_name in object_name:

                    # On active useOutlinerColor dans le attribut editor
                    cmds.setAttr(object_name + ".useOutlinerColor", True)

                    # On applique la couleur
                    # le nom de l'attribut est .outlinerColor
                    # Color contient la valeur de la
                    # couleur correspondant au key_name
                    # La couleur est une liste de 3 valeurs (RGB)
                    # on doit spécifie l'index pour
                    # avoir la couleur visuellement

                    cmds.setAttr(
                        object_name + ".outlinerColor",
                        color[0], color[1], color[2]
                    )
                    break

    def apply_reorder(self, data, objects):
        """Applique l'ordre alphabétique aux
        objets dans l'outliner selon le JSON.
        """
        # Création d'une liste vide pour contenir les objets à reorder
        objects_to_reorder = []

        # Parcout les objets dans maya
        for object_name in objects:

            # Parcourt les noms des keys dans le fichier JSON
            for key_name in data:

                # Si le nom de la key présentement parcourut
                # est dans le nom de l'objet présentement parcouru
                if key_name in object_name:

                    # On ajoute le nom de l'objet
                    # dans la liste d'objets à reorder
                    objects_to_reorder.append(object_name)
                    # Correspondance trouvée pour cet objet,
                    # alors on arrête de chercher dans les autres key_name
                    break

        # Avec la sélection, on n'a pas l'ordre alphabétique.

        # Il faut trier les objets avant de les réorganiser dans Maya
        # sorted_objects est la liste des
        # objets à reorder en ordre alphabetique
        sorted_objects = cmds.sortStringArray(
            objects_to_reorder, sortOrder="alphabetic"
        )

        # Parcourt tout les objets dans la
        # liste d'objets à reorder en orde alphabetique
        for object_name in sorted_objects:
            # Reorder les objets en ordre alphabetique
            # Ils sont placés dans le bas de la liste
            cmds.reorder(object_name, back=True)

    def organise_outliner(self):
        """Exécute les opérations sélectionnées et gère les Undo."""
        # Si aucune option est choisie, on affiche un message d'avertissement
        if (
            not self.apply_colors_checkbox.isChecked()
            and not self.apply_reorder_checkbox.isChecked()
        ):
            QMessageBox.warning(self, "WARNING", "Please select one operation")
            return

        # La fonction load_json est appellée
        # Création d'une variable locale pour stocker
        # les objets du fichier JSON retournés par load_json
        data = self.load_json()

        if data is None:
            return

        # Mets les modifications dans un même Undo
        cmds.undoInfo(openChunk=True, chunkName="Organise Outliner")

        # Protection si le programme plante.
        # Il faut fermer le undoInfo car s'il reste ouvert
        # et que sa plante ça peut causer des problèmes
        try:
            # La fonction get_objects est appellée
            # Création d'une variable locale pour
            # stocker les objets retournés par get_objects
            objects = self.get_objects()

            # Si ordrer est checked on applique
            # l'ordre sur les éléments sélectionnés
            if self.apply_reorder_checkbox.isChecked():
                self.apply_reorder(data, objects)

            # Si color est checked on applique
            # la color sur les éléments sélectionnés
            if self.apply_colors_checkbox.isChecked():
                self.apply_colors(data, objects)

        # À la fin peut importe ce qu'il arrive on ferme le closeChunk
        finally:
            cmds.undoInfo(closeChunk=True)

        cmds.outlinerEditor("outlinerPanel1", edit=True, refresh=True)

        # QMessageBox pour dire que l'opération est terminée
        message_done = QMessageBox(self)
        message_done.setIcon(QMessageBox.Information)
        message_done.setWindowTitle("Operation Done")
        message_done.setText("Organisation completed")
        message_done.addButton("Done", QMessageBox.AcceptRole)
        message_done.exec()


def main():
    """Fonction d'exécution principale de l'interface."""
    global ui_window
    try:
        ui_window.close()

    except Exception:
        pass

    # Création de ma fenêtre principale et appel de son constructeur
    ui_window = MainWindow()

    # Afficher la fenêtre principale car elle est caché par défaut
    ui_window.show()

# Vérifie si le ficher est standalone
if __name__ == "__main__":
    main()
