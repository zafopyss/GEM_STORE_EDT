
import re
import openpyxl as xl 
import pandas as pd
import numpy as np 
import warnings
import tkinter as ttk 

import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import filedialog as fd
from tkinter.messagebox import showinfo

warnings.filterwarnings('ignore', category=UserWarning, module='openpyxl')


def select_file():
    filename = fd.askopenfilename(
        initialdir='/Users/eliotwalter/Desktop' #chopper le lien ou se trouve le dossier + type de fichier 
    )
    if filename:
        showinfo(message=filename)
        path = filename
         

def get_value():
    date_choosen = current_var_combobox.get()
    week_choosen = week_days_combobox.get()

root = Tk()
frm = ttk.Frame(root, padding=10)
frm.grid()
#TO-DO // rentrer une base de données utilisateurs en amont dans tkinter : plusieurs fenêtres 
#TO-DO // dossier de selection pour excel + voir comment gérer les données entre les différents EDT : regrouper par groupe de classe 
#TO-DO // gérer l'UI de l'application 
#TO-DO // faire une flèche qui permet de changer le jour 
#TO-DO // gérer un planning avec nom + prénom à la fin du programme 
#TO-DO // voir comment gérer les électifs 
root.title('Programme')

current_var = ['23-10 au 29-10-2023', '30-10 au 05-11-2023', '06-11 au 12-11-2023'] #reprendre du programme 
current_var_grid = [2,1]

week_days = ["Lundi","Mardi","Mercredi","Jeudi","Vendredi"]
week_days_grid = [2,2]

ttk.Label(frm, text="Semaine : ").grid(column=0, row=0,sticky="n")
current_var_combobox = ttk.Combobox(values=current_var, state='readonly')
current_var_combobox.grid(column=1, row=0,sticky="n")
current_var_combobox.current(0)

ttk.Label(frm, text="Quel jour : ").grid(column=0, row=1,sticky="n")
week_days_combobox = ttk.Combobox(values=week_days, state='readonly')
week_days_combobox.grid(column=1, row=1)
week_days_combobox.current(0)
#récupérer les valeurs des combobox 

ttk.Button(frm,text="file",command=select_file).grid(column=0,row=4,sticky="se")
ttk.Button(frm,text="Rechercher").grid(column=2,row=2,sticky="sw")
ttk.Button(frm, text="Quit", command=root.destroy).grid(column=3, row=2,sticky="se")


root.mainloop()

day_to_number = {"lundi":"1","mardi":"2","mercredi":"3","jeudi":"4","vendredi":"5"}
planning_staff = [list(range(8,15)),list(range(14,21)),list(range(20,27)),list(range(26,33))]


def search_dispo(date_choosen): #rajouter nom et semaine 
    
    df1 = pd.read_excel(path,indice) #multithread à faire 

    print("C'est la semaine de "+df1.columns.tolist()[0] + ".") 


    list_staff_horaires = list(range(7,33))

    horaires1 = df1.iloc[1:57,0].dropna() 
    horaires2 = df1.iloc[1:57,7].dropna()
    horaires_total = pd.concat([horaires1,horaires2]).sort_values(ascending=True)#garder ces informations en mémoire car c'est toujours pareil 

    horaires_staff_total = horaires_total.iloc[list_staff_horaires]

    numero_jour = int(day_to_number[date_choosen]) #remplacer 
    day = df1.iloc[0:,[numero_jour]]
    day_index = day.dropna().index.tolist()
    print(day_index)
    try: 
        horaire_début_cours = min(day_index)
        horaire_fin_cours = max(day_index)+5
    except: 
        horaire_début_cours = 0
        horaire_fin_cours = 0
    horaires_cours = list(range(horaire_début_cours,horaire_fin_cours))

    horaires_de_staff = horaires_staff_total.index.tolist() #horaires de staff 
    horaires_dispo = list(set(horaires_de_staff) | set(horaires_cours))

    # Utilisez l'opérateur de soustraction pour obtenir les éléments qui ne sont présents que dans l'une des listes
    horaires_dispo = [x for x in horaires_dispo if (x not in horaires_cours or x not in horaires_de_staff) and  8 <= x <= 32] #horaires de staff dispo 

    for staff in planning_staff:
        if all(heures in horaires_dispo for heures in staff):
            print(f"tu peux staffer pour le {staff}") #changer ce que resort le programme à travers les heures : pas besoin 
        else: 
            print(f"ah jcrois tu peux pas staff pour ce moment : {staff}") 




