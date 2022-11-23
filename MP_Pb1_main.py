# -*- coding: utf-8 -*-
"""
Created on Wed Sep 28 09:32:23 2022

@author: Kévin Jousselin

Problème multiprocessing :
https://math.univ-angers.fr/~jaclin//site2023/lzNxo3B9R_ds2/concurrence/2023/multiprocessing/sequenceur/sequenceur.html


En ligne de commande, saisir :
    python3 ./MP_Pb1_main.py ./jobs 4       où 'jobs' est le dossier qui contient les jobs et '4' est le nb de processus
    ou bien
    python3 ./MP_Pb1_main.py                par défaut : dossier : ./jobs     Nb de processus : 4
"""


import sys
import time
import datetime
import multiprocessing
import importlib
import os
import random     # pour tester des exceptions de façon aléatoire


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
                
                # Test de lancement d'une exception 
                if random.randint(1,20)==1:
                    erreur
                
                t1 = time.time()
            
                # inscription au log
                with open(self.dossier_sortie+"/log.txt", 'a') as log:
                    log.write(f"Job {job_name:9}\t, lancé à {t_job}, par le processus n°{self.k+1:2d}, a durée {round(t1-t0,5):.5f} secondes.\n")
                
                print(f"Job {job_name:9}, lancé à {t_job}, par le processus n°{self.k+1:2d}, a durée {round(t1-t0,5):.5f} secondes.")                    
            
            except :
                # Ecriture du fichier xxxxx.result
                with open(self.dossier_sortie+'/'+job_name+".result", 'w') as f:
                    f.write(f"Une exception a été lancé.")
                
                # inscription au log
                with open(self.dossier_sortie+"/log.txt", 'a') as log:
                    log.write(f"Le job {job_name} a lancé une exception\n")
                print(f"Le job {job_name} a lancé une exception.")
                
                # Ajouter une exception dans la file
                MyProcess.queue_exception.put(1)
            


def main(dossier_jobs, dossier_sortie = './sortie_mp_pb1/', debug = False, display = False):

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
    
    # Création du dossier de sortie
    dossier_sortie = './sortie_mp_pb1/'
    os.makedirs(dossier_sortie, exist_ok=True)

    # Création du fichier log
    fichier_log = open(dossier_sortie+'/'+"log.txt", 'w')
    fichier_log.close()

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
    message = f'\n{Nb_fichiers} jobs taités par {Nb_processus} processus. Terminé en {round(T1-T0,2)} secondes avec {Nb_exception} exception(s).'
    with open(dossier_sortie+"/log.txt", 'a') as log:
        log.write(message)
    if display : print(message)
    if debug:    print("\nATTENTION : Ceci est le mode débug !!\n")



if __name__ == '__main__':
    
    # Récupérer les arguments en ligne de commande s'ils existent : nom du dossier et nombre de processus
    liste_arg = sys.argv
    try: 
        dossier_jobs = liste_arg[1]
        Nb_processus = int(liste_arg[2])
    except:     
        print()
        print("ATTENTION : \tLe format d'appel de la fonction doit être 'python3 ./probleme_un.py dossier_jobs Nb_processus")
        print("Par défault : dossier_jobs = './jobs/' et Nb_processus = 4")
        print()
        
        Nb_processus = 4
        dossier_jobs = './jobs'

    #Ajouter des dossiers au PATH
    sys.path.insert(0,'../jobs')
    sys.path.insert(0, '../jobs/modules')
    sys.path.insert(0,'./jobs')
    sys.path.insert(0,'./jobs/modules')
    sys.path.insert(0,dossier_jobs+'modules')
    sys.path.insert(0,dossier_jobs)
    
    # Lancement du programme principal
    main(dossier_jobs, display = True, debug = False)
