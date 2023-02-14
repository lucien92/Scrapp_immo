from shapely.geometry import Point
from shapely.geometry import Polygon, Point
import geopandas
import json
import pandas as pd

#on extrait les coordonnées du polygône de la maison de Clamart <3

contenance = 198

cadastre_path = "/home/lucien/Documents/scrapp_immo/cadastre-74281-parcelles.json"
with open(cadastre_path) as config_buffer:
        cadastre = json.loads(config_buffer.read())



#1) On récupère d'abord tous les polygônes correspondant au passerelle ayant la contenance indiquée
liste_id = []
for elem in cadastre["features"]:
    if "contenance" in elem["properties"]:
        test = elem["properties"]["contenance"]
        if test == contenance:
            liste_id.append(elem["id"])


#on récupère cet id grâce à la contenance du cadatsre que l'on met en entrée
list_polygone = []
for id_test in liste_id:
    for elem in cadastre["features"]: #cadastre["features"] est une liste de dictionnaires
        id = elem["id"]
        if id == id_test:
            polygone = elem["geometry"]["coordinates"]
            list_polygone.append(polygone)

#on veut transformer la liste de liste des polygônes en liste de tuples

L3 = []
for polygone in list_polygone:
    L2 = []
    for elem in polygone:
        for elem2 in elem:
            L2.append(tuple(elem2))
    polygon = Polygon(L2)
    L3.append(polygon)


adresse_path = "/home/lucien/Documents/scrapp_immo/adresses-74.csv"
df = pd.read_csv(adresse_path, sep=';')

#on effectue un tri en enlevant toutes les lignes dont la colonne id ne commence pas par 74281, i.e pas à thonon

df2 = df[df['id'].str.startswith('74281')]
latitude = df['lat']
longitude = df['lon']



#2)On localise les points qui se situent dans ou près des polynômes extraits

#on veut transformer la liste de liste en liste de tuples

L = []
for i in range(len(latitude)):
    L.append((longitude[i], latitude[i]))

#on veut trouver quel point de la liste L appartient aux polygones extraits

list_index = []
list_points = []
j = 0
for polygon in L3:
    j += 1
    for i in range(len(L)):
        point = Point(L[i])
        if point.within(polygon):
            list_points.append(L[i])
            list_index.append(j-1)

#on veut troiuver les points qui se situent à une distance inférieur à 0.00001 de l'un des polygones extraits

list_point2 = []
j = 0
for polygon in L3:
    j += 1
    bool = False
    for i in range(len(L)):
        #on veut trouver un moyen de perdre en complexité en éliminant les cas où ill est évident que le point est trop loin (prenons comme critère: le centre à plus de 0.001 d'un des coints du polygône)
        p1_test = p1 = (polygon.exterior.coords.xy[0][0], polygon.exterior.coords.xy[1][0]) #on extrait le premier point du  polygône et on le change en tuple
        p2_test = L[i]
        dist_test = dist = ((p2_test[0]-p1_test[0])**2 + (p2_test[1]-p1_test[1])**2)**(1/2)
        if dist_test > 0.01:
            continue
        else:
            t1 = Polygon(polygon)
            t = geopandas.GeoSeries(t1)
            t2 = geopandas.GeoSeries([Point(L[i])])
            dist = t.distance(t2)
            dist2 = dist[0]
            #faisons un algo qui va chercher les points qui se situent à une distance inférieur à 0.0005 de l'un des polygones extraits ou, s'il ne trouve rien, l'annonce, et va chercher le point le plus proche du polygône
            if dist2 < 0.0005: #Remarque: parfois quand on augmente trop la distance on récupère moins de numéro de parcelle. Avec 0.0005 on récupère 18 sur 18 dans le cas des 110m², mais dans d'autres cas?
                bool = True
                list_point2.append(L[i])
                list_index.append(j-1)


#on ajoute list_point2 à list_points 

for point in list_point2:
    if point not in list_points:
        list_points.append(point)


#3)Maintenant on récupère les adresses des points localisés

survivor = []       
for i in list_index:
    survivor.append(liste_id[i])

#on veut retrouver l'adresse de la maison en trouvant la valeur de numero et nom_voie correspondant à la ligne ou se trouve le point


j = 0
dic = {}
for i, points in enumerate(list_points):
    j += 1
    lon = points[0]
    lat = points[1]
    df2 = df.loc[(df["lon"] == lon) & (df["lat"] == lat), ["numero", "nom_voie"]] #manière claire de sélectionner des lignes et colonnes selon une liste de conditions séparées par des &
    numero = df2["numero"].values[0]
    nom_voie = df2["nom_voie"].values[0]
    if survivor[i][-4:] not in list(dic.keys()):
        dic[survivor[i][-4:]] = [(numero, nom_voie)]
    else:
        if (numero, nom_voie) not in dic[survivor[i][-4:]]:
            dic[survivor[i][-4:]].append((numero, nom_voie))

if j== 0:
    pass

dic2 = {}
for num in dic:
    dic2[num] = dic[num][0]

print(f'Dictionnaire avec les numéros de parcelle et les adresses: {dic2}' + '\n') #ce dictionnaire contient les numéros des parcelles faisant la taille demandée et les adresses potentielles des maisons correspondantes

print("ATTENTION: les adresses ne correspondent pas toujours à la parcelle mais sont topujours des adresses proches géographiquement de la vraie adresse, pour retrouver exactement l'adresse il faut regarder le numéro de parcelle donné par l'algo et voir sur géoportail l'adresse à laquelle il correspond " + '\n')

print(f'On devrait avoir une proposition de {len(liste_id)} maisons, mais on en a que {len(dic)} numéro de parcelle retrouvé avec des adresses potentielles'+ '\n')
