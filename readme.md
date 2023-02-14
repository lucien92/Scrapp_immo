# ***Algorithme pour retrouver des adresses dans Thonon-les-bains à partir de surface de passerelles à vendre***

## But du projet

Travail pour une agence immobilière dans le but de l'aider à retrouver les adresses des annonces sur des sites comme le bon coin, seulement en utilisant la surface du cadastre indiquée sur l'annonce (ainsi que la ville).
Pour cela on utilise les données trouvées sur les sites du gouvernement:
-https://cadastre.data.gouv.fr/datasets/cadastre-etalab pour les contenances des cadastres et les coordonnées des polygones correspondant
-https://adresse.data.gouv.fr/donnees-nationales pour les adresses et leur coordonnées sur un plan en latitude longitude

## **Approche du problème**

Au lieu de scrapper le site de géoportail nous avons préférer travailler directement à l'échelle des données fournies par le gouvernement via des fichiers json. Tout d'abord nous rentrons unne contenance de parcelle et nous extractons tous les polygônes d'une zone ayant cette surface. Nous utilisons les coordonnées des polygônes représentant les parcelles puis nous cherchons dans la base de données des points correspondant aux adresses pour voir quel point se situe dans le polygône cherché, ou au moins à une proximité très proche. Nous obtenons ainsi un dictionnaire qui associe des numéros de parcelle de la contenance recherchée à des adresses suspectes. Pour retrouver l'adresse axacte de la passerelle il suffit de rechercher l enuméro de parcelle indiqué dans le dictionnaire près de l'une des adresses.

## **Comment utiliser cet algorithme**

1) Rentrez la commande: pip install -r requirements.txt

2) Pour lancer l'algorithme sur Thonon-les-Bains rentrer la commande: python3 /chemin/vers/le/dossier/contenant/l'algorithme/polygon.py

exemple sur mon ordinateur: python3 /home/lucien/Documents/scrapp_immo/polygon.py

3) remarque: pour obtenir le chemin vers le fichier polygon.py, contenant l'algorithme, il suffit de faire un clique droit sur le fichier à gauche et de copier le chemin