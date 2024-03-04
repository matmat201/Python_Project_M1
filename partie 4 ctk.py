# -*- coding: utf-8 -*-
"""
Created on Fri Feb 23 16:50:32 2024

@author: mathi
"""
###############
#Import des bibliotheque
###############
from customtkinter import CTk, CTkLabel, CTkCheckBox, CTkSlider, CTkButton, CTkComboBox, IntVar, CTkFrame
import matplotlib.pyplot as plt
import numpy as np

# Importation des outils matplotlib pour créer zone graphique dans fenêtre tkinter 
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

import openpyxl as op

##############################################################################
# Fonctions pour convertir les valeurs du curseur en valeurs réelles
def scale_to_realmin(value):
    return value * 1e-4

def scale_to_realmax(value):
    return value * 1e2
##############################################################################
# Fonction pour mettre à jour l'affichage de la valeur réelle de tau
def update_value_tau(value, is_max=False):
    if is_max:
        real_value = scale_to_realmax(curseur_tau_max.get())
        label_valeur_tau_max.configure(text=f"     Valeur maximal de tau : {real_value:.4e}     ")
    else:
        real_value = scale_to_realmin(curseur_tau_min.get())
        label_valeur_tau_min.configure(text=f"     Valeur minimal de tau : {real_value:.4e}     ")
        
# Fonction pour mettre à jour l'affichage de la valeur réelle de l'energie
def update_value_nrj(value, is_max=False):
    if is_max:
        real_value = scale_to_realmax(curseur_nrj_max.get())
        label_valeur_nrj_max.configure(text=f"  Valeur maximal de l'energie : {real_value:.4e}  ")
    else:
        real_value = scale_to_realmin(curseur_nrj_min.get())
        label_valeur_nrj_min.configure(text=f"  Valeur minimal de l'energie : {real_value:.4e}  ")
##############################################################################
#fonction qui recupere le choix dans la combobox        
def choix_mat_fct(event):
    global mat_choisi
    mat_choisi = Menu_deroulant.get()
    print("Élément sélectionné :", mat_choisi)
##############################################################################    
def trace():
    # Lecture des datas
    book = op.load_workbook('bdd_photons_all_datas.xlsx')
    sheet = book.get_sheet_by_name(mat_choisi)

    Energie = []
    Diff_ela = []
    Diff_c = []
    Photoel = []
    CP_nuc = []
    CP_el = []
    Tot_w_ela = []
    Tot_wo_ela = []

    for i in range(4,sheet.max_row+1):                                  #on sait que les données commence a la 4ieme ligne
        Energie.append(float(sheet.cell(row = i, column = 1).value))
        Diff_ela.append(float(sheet.cell(row = i, column = 2).value))
        Diff_c.append(float(sheet.cell(row = i, column = 3).value))
        Photoel.append(float(sheet.cell(row = i, column = 4).value))
        CP_nuc.append(float(sheet.cell(row = i, column = 5).value))
        CP_el.append(float(sheet.cell(row = i, column = 6).value))
        Tot_w_ela.append(float(sheet.cell(row = i, column = 7).value))
        Tot_wo_ela.append(float(sheet.cell(row = i, column = 8).value))

    fig.clear() #On efface la zone graphique
    fig.canvas.draw() #On efface le canvas vide
    ax = fig.add_subplot(1,1,1) #graphe pleine page du canvas    
    ax.legend()
    ax.set_title(f"Evolution coeff atténuation massique pour {mat_choisi}")
    ax.set_xlabel("Energie")
    ax.set_ylabel("tau(cm2/g)")
    ax.set_xscale('log')
    ax.set_yscale('log')
    
    ax.set_xlim(scale_to_realmin(curseur_nrj_min.get()),scale_to_realmax(curseur_nrj_max.get()))
    ax.set_ylim(scale_to_realmin(curseur_tau_min.get()),scale_to_realmax(curseur_tau_max.get()))
    
    ax.grid(which = "major", axis='y', linestyle = '--')
    ax.grid(which = "both", axis='x', linestyle = '--')
    
    if PE_ctrl.get() == 1:
        ax.plot(Energie,Photoel,label="Effet photoélectrique")
    
    if Ray_ctrl.get() == 1:
        ax.plot(Energie,Diff_ela,label="Diffusion Rayleigh")
        
    if Comp_ctrl.get() == 1:
        ax.plot(Energie,Diff_c,label="Effet Compton")
        
    if CPn_ctrl.get() == 1:
        ax.plot(Energie,CP_nuc,label="Création de paire nucléaire")
        
    if CPe_ctrl.get() == 1:
        ax.plot(Energie,CP_el,label="Création de paire électronique")
        
    if TotSansRay_ctrl.get() == 1:
        ax.plot(Energie,Tot_wo_ela,label="Atténuation sans diffusion Rayleigh")
            
    if TotAvecRay_ctrl.get() == 1:
        ax.plot(Energie,Tot_w_ela,label="Atténuation avec diffusion Rayleigh")
        
    ax.legend()
    fig.canvas.draw()

    book.save('bdd_photons_all_datas.xlsx')
##############################################################################
def reset():
    fig.clear()
    ax = fig.add_subplot(1,1,1)
    ax.legend()
    ax.set_title(f"Evolution coeff atténuation massique pour {mat_choisi}")
    ax.set_xlabel("Energie")
    ax.set_ylabel("tau(cm2/g)")
    ax.set_xscale('log')
    ax.set_yscale('log')
    ax.set_xlim(scale_to_realmin(curseur_nrj_min.get()),scale_to_realmax(curseur_nrj_max.get()))
    ax.set_ylim(scale_to_realmin(curseur_tau_min.get()),scale_to_realmax(curseur_tau_max.get()))
    ax.grid(which = "major", axis='y', linestyle = '--')
    ax.grid(which = "both", axis='x', linestyle = '--')
    fig.canvas.draw()
    
    Menu_deroulant.set(list_materiaux[0])
    choix_mat_fct(None)
    
    PE_ctrl.set(0)
    Ray_ctrl.set(0)
    Comp_ctrl.set(0)
    CPn_ctrl.set(0)
    CPe_ctrl.set(0)
    TotSansRay_ctrl.set(0)
    TotAvecRay_ctrl.set(0)
    
    curseur_tau_min.set(1)
    curseur_tau_max.set(100)
    curseur_nrj_min.set(10)
    curseur_nrj_max.set(100)

##############
#Programme principal
##############

mat_choisi = "Aluminium"

#création d'une fenêtre tkinter
fenetre = CTk()
fenetre.geometry("1050x550")

#Titre à la fenêtre
fenetre.title("interactions des photon dans la matière")

#creation menu deroulant
Choix_mat = CTkLabel(fenetre, text="Choisir un élément Chimique :")
list_materiaux = ["Aluminium", "Plomb", "Cobalt", "Cuivre"]
Menu_deroulant = CTkComboBox(fenetre, values=list_materiaux,command=choix_mat_fct)
Menu_deroulant.set(list_materiaux[0])

#utilisation menu deroulant
#Menu_deroulant.bind("<<ComboboxSelected>>", choix_mat_fct)

#placement menu deroulant
Choix_mat.grid(row=0, column=0, sticky='w',padx=50)
Menu_deroulant.grid(row=0, column=1, sticky='w')

#creation variables de controle
PE_ctrl = IntVar()
Ray_ctrl = IntVar()
Comp_ctrl = IntVar()
CPn_ctrl = IntVar()
CPe_ctrl = IntVar()
TotSansRay_ctrl = IntVar()
TotAvecRay_ctrl = IntVar()

PE_ctrl.set(1)
Comp_ctrl.set(1)
CPn_ctrl.set(1)
CPe_ctrl.set(1)
TotSansRay_ctrl.set(1)

# Définir le poids des lignes et colonnes pour l'expansion automatique
fenetre.grid_rowconfigure(0, weight=1)
fenetre.grid_columnconfigure(0, weight=1)
fenetre.grid_rowconfigure(1, weight=1)
fenetre.grid_columnconfigure(1, weight=1)
fenetre.grid_rowconfigure(2, weight=1)
fenetre.grid_columnconfigure(2, weight=1)
fenetre.grid_rowconfigure(3, weight=1)
fenetre.grid_columnconfigure(3, weight=1)

#Creation du cadre selec courbe
cadre_courbe = CTkFrame(fenetre)
titre_cadre1 = CTkLabel(cadre_courbe, text="Cocher les courbes souhaitées :")
titre_cadre1.grid(row=0,sticky="nw",padx=25,pady=5)

#Creation des cases a cocher
PE_chk = CTkCheckBox(cadre_courbe, text="Effet photoélectrique", variable=PE_ctrl)
Ray_chk = CTkCheckBox(cadre_courbe, text="Diffusion Rayleigh", variable=Ray_ctrl)
Comp_chk = CTkCheckBox(cadre_courbe, text="Effet Compton", variable=Comp_ctrl)
CPn_chk = CTkCheckBox(cadre_courbe, text="Création de paire nucleaire", variable=CPn_ctrl)
CPe_chk = CTkCheckBox(cadre_courbe, text="Création de paire electronique", variable=CPe_ctrl)
TotSansRay_chk = CTkCheckBox(cadre_courbe, text="Atténuation sans diffusion Rayleigh", variable=TotSansRay_ctrl)
TotAvecRay_chk = CTkCheckBox(cadre_courbe, text="Atténuation avec diffusion Rayleigh", variable=TotAvecRay_ctrl)

#Placement des cases à cocher dans le cadre selec courbe
PE_chk.grid(row=1, sticky="w",pady=5)
Ray_chk.grid(row=2, sticky="w",pady=5)
Comp_chk.grid(row=3, sticky="w",pady=5)
CPn_chk.grid(row=4, sticky="w",pady=5)
CPe_chk.grid(row=5, sticky="w",pady=5)
TotSansRay_chk.grid(row=6, sticky="w",pady=5)
TotAvecRay_chk.grid(row=7, sticky="w",pady=5)

#Placement du cadre selec courbe
cadre_courbe.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

#creation cadre val tau
cadre_tau = CTkFrame(fenetre)
titre_cadre2 = CTkLabel(cadre_tau, text="Choisi les valeurs extremum de tau :")
titre_cadre2.grid(row=0,sticky="nw",padx=25,pady=5)

#creation des sliders tau
curseur_tau_min = CTkSlider(cadre_tau, from_=1, to=100, command=lambda value: update_value_tau(value, is_max=False))
label_valeur_tau_min = CTkLabel(cadre_tau, text="Valeur minimal de tau : ")
curseur_tau_min.set(1)
curseur_tau_min.grid(row=1, sticky="we")
label_valeur_tau_min.grid(row=2, sticky="we")

curseur_tau_max = CTkSlider(cadre_tau, from_=1, to=100, command=lambda value: update_value_tau(value, is_max=True))
label_valeur_tau_max = CTkLabel(cadre_tau, text="Valeur maximal de tau : ")
curseur_tau_max.set(100)
curseur_tau_max.grid(row=3, sticky="we")
label_valeur_tau_max.grid(row=4, sticky="we")

update_value_tau(curseur_tau_min.get(), is_max=False)
update_value_tau(curseur_tau_max.get(), is_max=True)

#placement du cadre tau
cadre_tau.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")

#creation cadre val energie
cadre_nrj = CTkFrame(fenetre)
titre_cadre3 = CTkLabel(cadre_nrj, text="Choisi les valeurs extremum de l'energie :")
titre_cadre3.grid(row=0,column=0,sticky="nw",padx=15,pady=5)

#creation des sliders
curseur_nrj_min = CTkSlider(cadre_nrj, from_=1, to=100, command=lambda value: update_value_nrj(value, is_max=False))
label_valeur_nrj_min = CTkLabel(cadre_nrj, text="Valeur minimal de l'énergie : ")
curseur_nrj_min.set(10)
curseur_nrj_min.grid(row=1, sticky="we")
label_valeur_nrj_min.grid(row=2, sticky="we")

curseur_nrj_max = CTkSlider(cadre_nrj, from_=1, to=100, command=lambda value: update_value_nrj(value, is_max=True))
label_valeur_nrj_max = CTkLabel(cadre_nrj, text="Valeur maximal de l'énergie : ")
curseur_nrj_max.set(100)
curseur_nrj_max.grid(row=3, sticky="we")
label_valeur_nrj_max.grid(row=4, sticky="we")

update_value_nrj(curseur_nrj_min.get(), is_max=False)
update_value_nrj(curseur_nrj_max.get(), is_max=True)

#placement du cadre energie
cadre_nrj.grid(row=2, column=1, padx=10, pady=10, sticky="nsew")

#Canva
fig = Figure(figsize=(6, 6))
graph = FigureCanvasTkAgg(fig, master=fenetre) 

canvas = graph.get_tk_widget() #Ajoute une zone graphe

#bouton fonction
Tracer_courbe_B = CTkButton(fenetre, text="Tracer les courbes",command=trace)
Reinitialis_B = CTkButton(fenetre, text="Réinitialiser",command=reset)
Quitter_B = CTkButton(fenetre, text="Quitter",command=fenetre.destroy)

#placement canva + dernier boutons:
Tracer_courbe_B.grid(row=3, column=0)
Reinitialis_B.grid(row=3,column=1)
Quitter_B.grid(row=3,column=2)

canvas.grid(row=1, column=2, rowspan=2, padx=10, pady=10, sticky="nsew")

#cadre des nouvelles fonctions#Creation du cadre selec courbe
cadre_nouv = CTkFrame(fenetre)
titre_cadre4 = CTkLabel(cadre_nouv, text="Nouvelles fonctions implémentée :")
titre_cadre4.grid(row=0,sticky="nw",padx=25,pady=5)
cadre_nouv.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")


Aide_B = CTkButton(cadre_nouv, text="Documentation",command=fenetre.destroy).grid(row=1,pady=5)
Coef_B = CTkButton(cadre_nouv, text="Extraction Tau",command=fenetre.destroy).grid(row=2,pady=5)
Section_B = CTkButton(cadre_nouv, text="Calcul Section Efficace",command=fenetre.destroy).grid(row=3,pady=5)
Unite_B = CTkButton(cadre_nouv, text="Changement unitée",command=fenetre.destroy).grid(row=4,pady=5)
Save_B = CTkButton(cadre_nouv, text="Sauvegarde Externe",command=fenetre.destroy).grid(row=5,pady=5)


#Détection action souris/clavier
fenetre.mainloop()
