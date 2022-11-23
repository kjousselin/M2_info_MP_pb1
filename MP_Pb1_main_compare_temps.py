# -*- coding: utf-8 -*-
"""
Created on Wed Sep 28 09:32:23 2022

@author: Kévin Jousselin

Problème multiprocessing :
https://math.univ-angers.fr/~jaclin//site2023/lzNxo3B9R_ds2/concurrence/2023/multiprocessing/sequenceur/sequenceur.html


En ligne de commande, saisir :
    python3 ./MP_Pb1_main.py ./jobs       où 'jobs' est le dossier qui contient les jobs et '4' est le nb de processus
    ou bien
    python3 ./MP_Pb1_main.py              par défaut : dossier : ./jobs     Nb de processus : 4

Remarque : dans ce programme j'ai retiré (mis en commentaire), l'écriture du log

"""


import sys
import time
import datetime
import multiprocessing
import importlib
import os
import random     # pour tester des exceptions de façon aléatoire
import matplotlib.pyplot as plt

class MyProcess(multiprocessing.Process):
    
    display = False                             # Affichage (ou non) des 'print' (non par défaut)
 
    queue_exception = multiprocessing.Queue()   # Création d'une file de partage : récupérer le nb d'exception
    
    def __init__(self, liste_jobs_name, k, dossier_sortie):
        multiprocessing.Process.__init__(self)   # Obligatoire
        self.liste_jobs_name = liste_jobs_name   
        self.k = k                               # numéro du processus
        self.dossier_sortie = dossier_sortie

    def run(self):
        
        # 'liste_jobs_name' contient une liste de modules à exécuter
        for job_name in self.liste_jobs_name:
            
            # Execution du job 'job_name'
            try:                
                t0 = time.time()
                
                # import du job et execution
                job = importlib.import_module(job_name, package = None)  # permet d'importer un module ou fichier dans une variable
                resultat = job.run()

                t_job = datetime.datetime.now()

                # Ecriture du fichier xxxxx.result
                with open(self.dossier_sortie+'/'+job_name+".result",'w') as f:
                    f.write(f"{resultat}")
                
                """
                # Test de lancement d'une exception 
                if random.randint(1,20)==1:
                    erreur
                """
                
                t1 = time.time()
                
                """
                # inscription au log
                with open(self.dossier_sortie+"/log.txt", 'a') as log:
                    log.write(f"Job {job_name:9}\t, lancé à {t_job}, par le processus n°{self.k+1:2d}, a durée {round(t1-t0,5):.5f} secondes.\n")
                
                if MyProcess.display:
                    print(f"Job {job_name:9}, lancé à {t_job}, par le processus n°{self.k+1:2d}, a durée {round(t1-t0,5):.5f} secondes.")                    
                """
                
            except :
                """
                # Ecriture du fichier xxxxx.result
                with open(self.dossier_sortie+'/'+job_name+".result", 'w') as f:
                    f.write(f"Une exception a été lancé.")
                
                # inscription au log
                if MyProcess.display:
                    with open(self.dossier_sortie+"/log.txt", 'a') as log:
                        log.write(f"Le job {job_name} a lancé une exception\n")
                    print(f"Le job {job_name} a lancé une exception.")
                
                # Ajouter une exception dans la file
                MyProcess.queue_exception.put(1)
                """
                pass
            

def main(dossier_jobs, dossier_sortie = './sortie_mp_pb1/', debug = False, display = False, Nb_processus = 10):
    """
    
    Cette fonction exécute tous les jobs répartis sur 'Nb_processus' processus
    
    """
    
    T0 = time.time()

    # Mode débugage pour tests : limite à 50 jobs 
    if debug: 
        print()
        print("ATTENTION : Lancé en mode débug !!")    

    # Parcours de tous les fichiers du dossier 'dossier_jobs'
    listeFichiers = []
    for (repertoire, sousRepertoires, fichiers) in os.walk(dossier_jobs):
        for names in fichiers:
            if names[:4]=='jobs' and names[-3:]=='.py':
                listeFichiers.append(names[:-3])
                
    """
    # Création du fichier log
    fichier_log = open(dossier_sortie+'/'+"log.txt", 'w')
    fichier_log.close()
    """

    # En mode debug : test de lecture de 50 fichiers
    if debug: listeFichiers = listeFichiers[:50]   

    Nb_fichiers = len(listeFichiers)    
    liste_processus = [] # liste de tache      

    # Dispatch des jobs pour les Nb_processus processus, puis chargement des processus dans une liste
    if display : print('Chargement des processus :')
    for k in range(Nb_processus):
        L_for_1_proc = listeFichiers[k::Nb_processus]   # Contient la liste des jobs destinés au processus n°k
        liste_processus.append(MyProcess(L_for_1_proc, k, dossier_sortie))    
    if display : 
        print('terminé')
        MyProcess.display = True
        
    # Lancement des processus
    if display : print('Lancement des processus :')
    for processus in liste_processus:
        processus.start()  
    if display : print('terminé')

    # Attente des processus
    if display : print('Attente des processus :')
    for processus in liste_processus:
        processus.join()   # La méthode join bloque la suite du programme
                           # tant que le programme 'processus' n'est pas terminé

    T1 = time.time()

    # Compter les exceptions (récupérée dans une file)
    Nb_exception = 0
    while not MyProcess.queue_exception.empty():
        Nb_exception += MyProcess.queue_exception.get()

    # Bilan
    """
    message = f'\n{Nb_fichiers} jobs taités par {Nb_processus} processus. Terminé en {round(T1-T0,2)} secondes avec {Nb_exception} exception(s).'
    with open(dossier_sortie+"/log.txt", 'a') as log:
        log.write(message)
    if display : print(message)
    if debug:    print("\nATTENTION : Ceci est le mode débug !!\n")
    """
    
    return(T1-T0)   # Temps de traitement de tous les jobs



def Compare_temps(N = 20, debug = False):
    """
    
    - Cette fonction lance plusieurs fois le 'main' avec un nombre de 
    processus variant entre 0 et N.
    
    - Affiche et consigne les résultats dans un fichier Temps.txt
    
    - Représente graphiquement les résultats en affichant le temps en fonction du nombre de processus
    
    """
    
    Temps = []
    
    # Création du dossier de sortie
    dossier_sortie = './sortie_mp_pb1/'
    os.makedirs(dossier_sortie, exist_ok=True)
    
    print("Veuillez patienter quelques minutes entre chaque découpage...")
    
    # Création du fichier 'Temps.txt' (bilan)
    fichier_temps = open(dossier_sortie+'/'+"Temps.txt", 'w')
    fichier_temps.close()
    
    # Exécution de 'main' pour Nb_processus allant de 1 à N
    for k in range(1, N):
        print(f"Pour un découpage en {k} processus : ")
        duree = main(dossier_jobs, display = False, debug = debug, Nb_processus = k)
        Temps.append(duree)
        print(f"le temps de calcul est {Temps[-1]}")

        # Ajout d'une ligne dans le fichier bilan
        with open(dossier_sortie+"/Temps.txt", 'a') as f:
            f.write(f"Pour un découpage en {k} processus : \t le temps de calcul est {Temps[-1]}\n")

    # Représentation graphique des résultats        
    plt.plot(range(1,N), Temps, 'x', label = 'Temps de traitement en fonction du nb de processus')
    plt.title(f"Multiprocessing problème 1 : traitement des jobs.")
    plt.xlabel("Nb de processus")
    plt.ylabel("Temps de calcul (seconde)")
    plt.legend()
    plt.show()


if __name__ == '__main__':
    
    # Récupérer les arguments en ligne de commande s'ils existent : nom du dossier et nombre de processus
    liste_arg = sys.argv
    try: 
        dossier_jobs = liste_arg[1]
    except:     
        print()
        print("ATTENTION : \tLe format d'appel de la fonction doit être 'python3 ./MP1....py dossier_jobs")
        print("Par défault : dossier_jobs = './jobs/'")
        print()
        dossier_jobs = './jobs'

    #Ajouter des dossiers au PATH
    sys.path.insert(0,'../jobs')
    sys.path.insert(0, '../jobs/modules')
    sys.path.insert(0,'./jobs')
    sys.path.insert(0,'./jobs/modules')
    sys.path.insert(0,dossier_jobs+'modules')
    sys.path.insert(0,dossier_jobs)
        
    # Lancement du programme principal
    Compare_temps(debug = False)

