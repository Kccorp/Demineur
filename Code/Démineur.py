# coding: utf8

from tkinter import *
from tkinter.messagebox import *
import math
import random
import tkinter.font as tkFont
import time

table = []
table_button = []
table_drapeau = []

menu = Tk()
menu.geometry("400x600")
menu.title("Projet démineur")
menu["bg"] = "#C3C3C3"
menu.resizable(width=False, height=False)


def grille_analyse(colonne, ligne):
    # cases interieurs
    for x in range(1, colonne - 1):
        for y in range(1, ligne - 1):
            listeB = [
                table[x - 1][y - 1],
                table[x][y - 1],
                table[x + 1][y - 1],
                table[x - 1][y],
                table[x + 1][y],
                table[x - 1][y + 1],
                table[x][y + 1],
                table[x + 1][y + 1]
            ]

            if table[x][y] != "B":
                table[x][y] = listeB.count("B")

    # cÃƒÆ’Ã‚Â´tÃƒÆ’Ã‚Â© gauche
    for x in range(1, colonne - 1):
        for y in range(0, 1):
            listeB2 = [
                table[x - 1][y],
                table[x + 1][y],
                table[x - 1][y + 1],
                table[x][y + 1],
                table[x + 1][y + 1]
            ]
            if table[x][y] != "B":
                table[x][y] = listeB2.count("B")

    # cÃƒÆ’Ã‚Â´tÃƒÆ’Ã‚Â© haut
    for x in range(0, 1):
        for y in range(1, ligne - 1):
            listeB3 = [
                table[x][y - 1],
                table[x][y + 1],
                table[x + 1][y - 1],
                table[x + 1][y],
                table[x + 1][y + 1]
            ]
            if table[x][y] != "B":
                table[x][y] = listeB3.count("B")

    # cÃƒÆ’Ã‚Â´tÃƒÆ’Ã‚Â© droit
    for x in range(1, colonne - 1):
        for y in range(ligne - 1, ligne):
            listeB4 = [table[x - 1][y - 1], table[x - 1][y], table[x][y - 1], table[x + 1][y - 1], table[x + 1][y]]
            if table[x][y] != "B":
                table[x][y] = listeB4.count("B")

    # cÃƒÆ’Ã‚Â´tÃƒÆ’Ã‚Â© bas
    for x in range(colonne - 1, colonne):
        for y in range(1, ligne - 1):
            listeB5 = [table[x - 1][y - 1], table[x - 1][y], table[x - 1][y + 1], table[x][y - 1], table[x][y + 1]]
            if table[x][y] != "B":
                table[x][y] = listeB5.count("B")

    # coin haut-gauche
    for x in range(0, 1):
        for y in range(0, 1):
            listeB6 = [table[x][y + 1], table[x + 1][y], table[x + 1][y + 1]]
            if table[x][y] != "B":
                table[x][y] = listeB6.count("B")

    # coin haut-droit
    for x in range(0, 1):
        for y in range(ligne - 1, ligne):
            listeB7 = [table[x][y - 1], table[x + 1][y - 1], table[x + 1][y]]
            if table[x][y] != "B":
                table[x][y] = listeB7.count("B")

        # coin bas-gauche
        for x in range(colonne - 1, colonne):
            for y in range(0, 1):
                listeB8 = [table[x - 1][y], table[x - 1][y + 1], table[x][y + 1]]
                if table[x][y] != "B":
                    table[x][y] = listeB8.count("B")

        # coin bas-droit
        for x in range(colonne - 1, colonne):
            for y in range(ligne - 1, ligne):
                listeB9 = [table[x - 1][y - 1], table[x - 1][y], table[x][y - 1]]
                if table[x][y] != "B":
                    table[x][y] = listeB9.count("B")


def Démineur(colonne, ligne):
    global nbr_bombe_rest

    nbr_bombe_rest = nbrBomb
    print(nbr_bombe_rest)

    def looser(x, y, monCanvas):
        if table[x][y] == "B":
            for y in range(colonne):
                if table[y][x] == "B":
                    table_button[y][x].destroy()
                for x in range(ligne):
                    if table[y][x] == "B":
                        table_button[y][x].destroy()

            Defaite = Tk()
            Defaite.title("Défaite")
            Defaite.geometry("200x200")
            Defaite["bg"] = "#C3C3C3"

            Perdu = LabelFrame(Defaite, borderwidth=2, text="Vous avez perdu !", fg='black', bg='#C3C3C3',
                               labelanchor="n")
            Perdu.pack(padx=20, pady=20)

    def winner():
        global case_restante
        if case_restante == nbrBomb:
            Win = Tk()
            Win.title("Win")
            Win.geometry("200x200")
            Win["bg"] = "#C3C3C3"

            Gagner = LabelFrame(Win, borderwidth=2, text="Vous avez Gagné !", fg='black', bg='#C3C3C3', labelanchor="n")
            Gagner.pack(padx=20, pady=20)

    def drapeau(x, y):
        global nbr_bombe_rest
        if table_drapeau[x][y] == True:
            table_button[x][y].configure(bg="salmon", state="normal")
            table_drapeau[x][y] = False
            nbr_bombe_rest += 1
            label_bomb()
        else:
            table_drapeau[x][y] = False
            if table_drapeau[x][y] == False:
                table_drapeau[x][y] = True
                table_button[x][y].configure(bg="red", state="disable")
                nbr_bombe_rest -= 1
                label_bomb()

    # Création canvas
    fen_princ = Tk()
    fen_princ.title("Projet démineur")
    fen_princ.geometry("800x850")
    fen_princ["bg"] = "#C3C3C3"

    monCanvas = Canvas(fen_princ, width=ligne, height=colonne, bg='ivory', bd=0, highlightthickness=0)
    monCanvas.place(x=25, y=25)

    # Affichage timer + nombre de bombe restante
    def label_bomb():
        print(nbr_bombe_rest)
        decompte_mines.configure(text=nbr_bombe_rest)

    decompte_mines = Label(fen_princ, text="", fg='red')
    decompte_mines.pack()
    label_bomb()

    # Init_Clock
    def makeWidgets():
        global timer
        timer = Label(fen_princ, text="", fg='red')
        setTime(elapsedtime)
        timer.place(width=20, height=20, x=40)
        Start()

    def update():
        elapsedtime = time.time() - start
        setTime(elapsedtime)
        timer.after(50, update)

    def setTime(elap):
        minutes = int(elap / 60)
        seconds = int(elap - minutes * 60.0)
        timestr = ('%03d' % (seconds))
        timer.configure(text=timestr)

    def Start():
        global start
        start = 0.0
        start = time.time() - elapsedtime
        update()

    elapsedtime = 0.0
    timestr = StringVar()
    makeWidgets()

    def compter_global(x, y):
        global case_restante

        def compter_haut(x, y):
            global case_restante
            if x != -1:
                if table[x][y] == 0:
                    print("exist : ", "(", x, y, ")", table_button[x][y].winfo_exists())
                    if table_button[x][y].winfo_exists() == 1:
                        table_button[x][y].destroy()
                        print("exist : ", "(", x, y, ")", table_button[x][y].winfo_exists())
                        case_restante -= 1
                        print("case restante, haut :", case_restante)
                        compter_gauche(x, y - 1)
                        compter_droit(x, y + 1)
                        compter_haut(x - 1, y)
                        if table[x - 1][y] != 0 and table[x][y] != "B":
                            if x != 0:
                                table_button[x - 1][y].destroy()
                                case_restante -= 1
                                print("case restante, haut more :", case_restante)

                        # coins :
                        if x != 0 and y != ligne - 1:
                            if table[x - 1][y + 1] != 0 and table[x - 1][y + 1] != "B":
                                table_button[x - 1][y + 1].destroy()  # haut droite
                                case_restante -= 1
                                print("case restante, haut droite :", x, y, case_restante)
                        elif x != 0 and y != 0:
                            if table[x - 1][y - 1] != 0 and table[x - 1][y - 1] != "B":
                                table_button[x - 1][y - 1].destroy()  # haut gauche
                                case_restante -= 1
                                print("case restante, haut gauche :", x, y, case_restante)

        def compter_bas(x, y):
            global case_restante
            if x != colonne:
                if table[x][y] == 0:
                    if table_button[x][y].winfo_exists() == 1:
                        table_button[x][y].destroy()
                        case_restante -= 1
                        print("case restante, bas :", x, y, case_restante)
                        compter_gauche(x, y - 1)
                        compter_droit(x, y + 1)
                        compter_bas(x + 1, y)
                        if x + 1 != colonne:
                            if table[x + 1][y] != 0 and table[x + 1][y] != "B":
                                table_button[x + 1][y].destroy()
                                case_restante -= 1
                                print("case restante, gauche more :", case_restante)

                        # coins :
                        if x != colonne - 1 and y != ligne - 1:
                            if table[x + 1][y + 1] != 0 and table[x + 1][y + 1] != "B":
                                table_button[x + 1][y + 1].destroy()  # bas droite
                                case_restante -= 1
                                print("case restante, bas droite :", x, y, case_restante)
                        elif x != colonne - 1 and y != 0:
                            if table[x + 1][y - 1] != 0 and table[x + 1][y - 1] != "B":
                                table_button[x + 1][y - 1].destroy()  # bas gauche
                                case_restante -= 1
                                print("case restante, bas gauche :", x, y, case_restante)

                elif x == colonne - 1:
                    table_button[colonne - 1][y].destroy()
                    case_restante -= 1
                    print("case restante, bas more :", x, y, case_restante)

        def compter_gauche(x, y):
            global case_restante
            if y != -1:
                if table[x][y] == 0:
                    if table_button[x][y].winfo_exists() == 1:
                        table_button[x][y].destroy()
                        case_restante -= 1
                        print("case restante, gauche :", case_restante)
                        compter_gauche(x, y - 1)
                elif y != 0:
                    if table[x][y] != 0 and table[x][y] != "B":
                        table_button[x][y].destroy()
                        case_restante -= 1
                        print("case restante, gauche more :", case_restante)

        def compter_droit(x, y):
            global case_restante
            if y != ligne:
                if table[x][y] == 0:
                    if table_button[x][y].winfo_exists() == 1:
                        table_button[x][y].destroy()
                        case_restante -= 1
                        print("case restante, droit :", case_restante)
                        compter_droit(x, y + 1)
                elif y != ligne - 1:
                    if table[x][y] != 0 and table[x][y] != "B":
                        table_button[x][y].destroy()
                        case_restante -= 1
                        print("case restante, droit morte :", case_restante)

                elif y == ligne - 1:
                    table_button[x][ligne - 1].destroy()
                    case_restante -= 1
                    print("case restante, droit more :", case_restante)

        if table[x][y] == 0:
            compter_haut(x, y)
            compter_bas(x + 1, y)
        else:
            table_button[x][y].destroy()
            case_restante -= 1
            print("case restante :", case_restante)

    # Création et analyse des bombes
    for y in range(colonne):
        liste = []
        for x in range(ligne):
            text = [0]
            liste.append(text)
        table.append(liste)

    for k in range(nbrBomb):
        x = random.randint(0, ligne - 1)
        y = random.randint(0, colonne - 1)
        table[y][x] = "B"

        grille_analyse(colonne, ligne)

        # Affichage du texte derrière les bombes
        h = 0
    for x in range(colonne):
        l = 0
        for y in range(ligne):
            liste1 = table[h]
            Text = liste1[l]
            TEXT = Button(monCanvas, width=2, relief=FLAT, state=DISABLED, text="I")
            TEXT.grid(row=x, column=y)
            TEXT.configure(text=Text)
            if table[x][y] == 0:
                TEXT.configure(text=" ")
            l += 1
        h += 1

    for i in range(colonne):
        table_button.append([])
        table_drapeau.append([])
        for j in range(ligne):
            button = Button(monCanvas, bg='salmon', width=2)
            button.click = False
            button.configure(
                command=lambda x=i, y=j: [print("{} , {} : {}".format(x, y, table[x][y])),
                                          looser(x, y, monCanvas), compter_global(x, y), winner()])

            button.bind("<Button-3>", lambda f=1, x=i, y=j: [print(x, y, nbrBomb), drapeau(x, y)])
            button.grid(row=i, column=j)
            table_button[i].append(button)
            table_drapeau[i].append(button)

    # Affichage de la liste
    for k in range(colonne):
        print(table[k], "\n")

    monCanvas.mainloop()


def option():
    def Vérification():
        global nbrBomb, case_restante
        colonne = colonne1.get()
        ligne = ligne1.get()
        nbrBomb = nbrBomb1.get()
        case_restante = colonne * ligne
        print(case_restante)
        while True:
            if colonne > 24:
                colonne = 24
                print("/!/")
            elif ligne > 30:
                ligne = 30
                print("/?/")
                print(ligne)
            elif nbrBomb > 667:
                nbrBomb = 667
            elif colonne <= 24 or ligne <= 30:
                option.quit()
                Démineur(colonne, ligne)
                break

    option = Tk()
    option["bg"] = "#C3C3C3"
    option.title("Projet démineur")
    option.resizable(width=False, height=False)

    def Personalisé():
        if varPerso.get() == 1:

            CaseDébutant.deselect()
            CaseIntermédiaire.deselect()
            CaseExpert.deselect()

            cadre_Bombe.pack(side=RIGHT, padx=20, pady=20)
            cadre_long.pack(side=LEFT, padx=20, pady=20)
            cadre_larg.pack(side=LEFT, padx=20, pady=20)

        elif varPerso.get() == 0:
            cadre_Bombe.pack_forget()
            cadre_larg.pack_forget()
            cadre_long.pack_forget()

    def Débutant():
        if varDébutant.get() == 1:
            CasePerso.deselect()
            CaseIntermédiaire.deselect()
            CaseExpert.deselect()

            Personalisé()

            colonne1.set(9)
            ligne1.set(9)
            nbrBomb1.set(10)

    def Intermédiaire():
        if varIntermédiaire.get() == 1:
            CasePerso.deselect()
            CaseDébutant.deselect()
            CaseExpert.deselect()

            Personalisé()
            colonne1.set(16)
            ligne1.set(16)
            nbrBomb1.set(40)

    def Expert():
        if varExpert.get() == 1:
            CasePerso.deselect()
            CaseDébutant.deselect()
            CaseIntermédiaire.deselect()

            Personalisé()
            colonne1.set(16)
            ligne1.set(30)
            nbrBomb1.set(99)

    # Label colonnes
    cadre_larg = LabelFrame(option, borderwidth=2, text="Hauteur ", fg='black', bg='#C3C3C3', labelanchor="nw")

    Label_larg = Label(cadre_larg, bg='#C3C3C3')
    Label_larg.pack()
    # Set nbr colonnes
    colonne1 = IntVar()
    Champ_larg = Entry(Label_larg, text=colonne1, bg="white")
    Champ_larg.pack(padx=5, pady=5)
    Champ_larg.focus_set()

    # Label lignes
    cadre_long = LabelFrame(option, borderwidth=2, text="Largeur ", fg='black', bg='#C3C3C3', labelanchor="nw")

    Label_long = Label(cadre_long, bg='#C3C3C3')
    Label_long.pack()
    # Set nbr lignes
    ligne1 = IntVar()
    Champ_long = Entry(Label_long, textvariable=ligne1, bg="white")
    Champ_long.pack(padx=5, pady=5)
    Champ_long.focus_set()

    # Label bombes
    cadre_Bombe = LabelFrame(option, borderwidth=2, text="Nombre de Bombes ", fg='black', bg='#C3C3C3',
                             labelanchor="nw")

    Label_Bombe = Label(cadre_Bombe, bg='#C3C3C3')
    Label_Bombe.pack()
    # Set nbr bombes
    nbrBomb1 = IntVar()
    Champ_Bombe = Entry(Label_Bombe, textvariable=nbrBomb1, bg="white")
    Champ_Bombe.focus_set()
    Champ_Bombe.pack(padx=5, pady=5)

    # Checkbox

    # Chech_débutant
    varDébutant = IntVar()
    CaseDébutant = Checkbutton(option, text='Débutant', variable=varDébutant, command=Débutant)
    CaseDébutant.pack(side=LEFT, padx=20, pady=20)

    # Check_Intermédiaire
    varIntermédiaire = IntVar()
    CaseIntermédiaire = Checkbutton(option, text='Intermédiaire', variable=varIntermédiaire, command=Intermédiaire)
    CaseIntermédiaire.pack(side=LEFT, padx=20, pady=20)

    # Check_Expert
    varExpert = IntVar()
    CaseExpert = Checkbutton(option, text='Expert', variable=varExpert, command=Expert)
    CaseExpert.pack(side=LEFT, padx=20, pady=20)

    # Check_Perso
    varPerso = IntVar()
    CasePerso = Checkbutton(option, text='Personalisé..', variable=varPerso, command=Personalisé)
    CasePerso.pack(side=LEFT, padx=20, pady=20)

    # Bouton Valider
    Valider = Button(option, text="Valider", relief=RAISED, command=Vérification, bg='#C3C3C3')
    Valider.pack(side=RIGHT, padx=10, pady=10)


def command():
    menu.destroy()
    option()


img = PhotoImage(file="th.png")

image = Canvas(menu, bg='#C3C3C3', highlightthickness=0)
image.create_image(195, 150, image=img)
image.pack()

police = tkFont.Font(size=20)
Jouer = Button(menu, text="Nouvelle Partie", relief=RAISED, borderwidth=5, fg="red", width=20, font=police,
               bg='#C3C3C3', command=command)
Jouer.pack(pady='70')

Quitter = Button(menu, text="Quitter", relief=RAISED, command=menu.destroy, bg='#C3C3C3')
Quitter.pack(side=BOTTOM, padx=10, pady=10)

cadre_nom = LabelFrame(menu, borderwidth=2, text="Nom", fg='black', bg='#C3C3C3', labelanchor="nw")
cadre_nom.pack(side=BOTTOM, padx=20, pady=20)

Label_nom = Label(cadre_nom, bg='#C3C3C3')
Label_nom.pack()

Nom = StringVar()
Champ = Entry(Label_nom, textvariable=Nom, bg="white")
Champ.focus_set()
Champ.pack(padx=5, pady=5)

menu.mainloop()


