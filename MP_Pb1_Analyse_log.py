# -*- coding: utf-8 -*-
"""
Created on Wed Sep 28 11:34:10 2022

@author: Kévin Jousselin


1) Choisir le dossier du log
2) Choisir le nom du fichier du log
3) Exécuter le script

"""

######################## ANALYSE DU LOG ########################

import re

dossier = './sortie_mp_pb1/'
fichier = 'log.txt'

Ordre_processus = []
liste_temps = []

# Ouverture du log
with open(dossier+fichier, encoding='utf8') as f:
    for ligne in f:
        
        # Lecture des lignes contenant l'information
        if ligne[:4] == 'Job ':
            # expression régulière recherchée
            regex = r"n° ([0-9]+).* ([0-9]+\.[0-9]+) secondes." 
            trouve = re.findall(regex, ligne)
            
            # Numéro du processus 
            num_processus = int(trouve[0][0])    
            
            # Temps d'execution
            temps = float(trouve[0][1])   
            liste_temps.append(temps)
            
            # Ordre d'éxécution des processus
            Ordre_processus.append(num_processus)


######################## VISUALISATION DES RESULTATS ########################

import matplotlib.pyplot as plt


# Configuration de la fenêtre graphique
plt.figure(figsize=(12, 5))
plt.ylabel("Numéro du processes")
plt.xlabel("Durée d'une tâche en secondes")
plt.title('Analyse du log : Temps de calcul de chaque job, répartis selon leur processus.')
haut = 1
width = 0.6
color_dict = {0:'red', 1:'green', 2:'blue', 3:'yellow', 4:'orange'}

Nb_process = max(Ordre_processus)
left = [0]*Nb_process               # left contient, pour chaque processus, le décalage indiquant où commence la nouvelle barre

# Construction des barres    
for k in range(len(Ordre_processus)):
    rect = plt.barh(Ordre_processus[k], liste_temps[k], width, left = left[Ordre_processus[k]-1], label=k,color=color_dict[k%5]) 
    left[Ordre_processus[k]-1] += liste_temps[k]   
    #plt.legend()

plt.show()

