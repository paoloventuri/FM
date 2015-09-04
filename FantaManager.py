from tkinter            import *
from tkinter            import messagebox, ttk
from league_manager     import LeagueManager as LM
from stat_downloader    import StatDownloader
from autocomplete_entry import AutocompleteEntry
from pdf_creator        import PdfCreator
import re, os

class FantaManager():
    def __init__(self):
        self.select_league()

    def check_folders(self):
        os.makedirs("json", exist_ok=True)
        os.makedirs("json/leagues", exist_ok=True)

    def set_icon(self, fin):
        img = PhotoImage(file='FM')
        fin.tk.call('wm', 'iconphoto', fin._w, img)

    def exit(self):
        a = messagebox.askyesno(title = "Uscita da FM", message = "Vuoi veramente uscire da FM?")
        if a:
            self.main_f.destroy()

    def confirm_league(self):
        if self.lega.get() == "":
            messagebox.showwarning(title = "FM - Errore", message = "Nessuna lega selezionata")
        else:
            self.main_f.destroy()
            self.lm = LM(self.lega.get())
            self.lm.load_league()
            self.home_page()

    def delete_league(self):
        if self.lega.get() == "":
            messagebox.showwarning(title = "FM - Errore", message = "Nessuna lega selezionata")
        else:
            a = messagebox.askyesno(title = "FM - Elimina lega", message = "Vuoi veramente eliminare la lega: " + self.lega.get() + "?")
            if a:
                self.main_f.destroy()
                self.lm = LM(self.lega.get())
                self.lm.delete_league()
                self.select_league()

    def new_league(self):
        self.new_league_f =Toplevel()
        self.new_league_f.geometry("400x200+400+200")
        self.new_league_f.title("FM - Inserisci nuova lega")

        l = Label(self.new_league_f, text = "Inserisci il nome della nuova lega", font=("Helvetica", 16))
        l.pack(fill = X, pady = (20, 20))

        self.n = Entry(self.new_league_f)
        self.n.focus()
        self.n.pack(fill = X)

        bn = Frame(self.new_league_f)
        insertB = Button(bn, text = "Inserisci", command = self.insert_new_name)
        insertB.pack(side = RIGHT, pady = (20, 20), padx = (10 ,10))
        bn.pack(side=BOTTOM, fill=X)
        
        self.set_icon(self.new_league_f)
        self.new_league_f.mainloop()

    def insert_new_name(self):
        self.name = self.n.get()

        if self.name == "" :
            self.new_league_f.destroy()
        
        elif self.name in self.leagues:
            messagebox.showwarning(title = "FM - Errore", message = "Il nome della lega è già utilizzato")
            self.new_league_f.destroy()

        else:
            self.new_league_f.destroy()
            self.insert_rules()

    def insert_rules(self):
        self.insert_league_f =Toplevel()
        self.insert_league_f.geometry("400x400+400+200")
        self.insert_league_f.title("FM - Inserisci regole")

        l = Label(self.insert_league_f, text = "Inserisci le regole della nuova lega", font=("Helvetica", 16))
        l.pack(fill = X, pady = (20, 20))

        por_l = Label(self.insert_league_f, text = "Numero di portieri:", font=("Helvetica", 8))
        por_l.pack(fill = X)
        self.por = Spinbox(self.insert_league_f, from_ = 1, to = 10)
        self.por.pack()

        dif_l = Label(self.insert_league_f, text = "Numero di difensori:", font=("Helvetica", 8))
        dif_l.pack(fill = X)
        self.dif = Spinbox(self.insert_league_f, from_ = 6, to = 20)
        self.dif.pack()

        cen_l = Label(self.insert_league_f, text = "Numero di centrocampisti:", font=("Helvetica", 8))
        cen_l.pack(fill = X)
        self.cen = Spinbox(self.insert_league_f, from_ = 6, to = 20)
        self.cen.pack()

        att_l = Label(self.insert_league_f, text = "Numero di attaccanti:", font=("Helvetica", 8))
        att_l.pack(fill = X)
        self.att = Spinbox(self.insert_league_f, from_ = 4, to = 12)
        self.att.pack()

        mod_l = Label(self.insert_league_f, text = "Si vuole utilizzare il modificatore della difesa?", font=("Helvetica", 8))
        mod_l.pack(fill = X)
        self.mod = Spinbox(self.insert_league_f, values = ("Si" , "No"))
        self.mod.pack()        

        bn = Frame(self.insert_league_f)
        insertB = Button(bn, text = "Inserisci", command = self.create_league)
        insertB.pack(side = RIGHT, pady = (20, 20), padx = (10 ,10))
        bn.pack(side=BOTTOM, fill=X)
        
        self.set_icon(self.insert_league_f)
        self.insert_league_f.mainloop()

    def create_league(self):
        n_por = int(self.por.get())
        n_dif = int(self.dif.get())
        n_cen = int(self.cen.get())
        n_att = int(self.att.get())
        if self.mod.get() == "Si" : 
            mod = True 
        else: mod = False

        self.lm = LM(self.name)
        self.lm.create_league(n_por, n_dif, n_cen, n_att, mod)
        self.insert_league_f.destroy()
        self.main_f.destroy()
        self.home_page()

    def select_league(self):
        self.check_folders()
        self.main_f = Tk()
        self.main_f.geometry("800x400+200+100")
        self.main_f.title("FM - Selezione lega")
        

        l = Label(self.main_f, text = "Seleziona la lega che vuoi gestire", font=("Helvetica", 16))
        l.pack(fill = X, pady = (20, 20))

        self.leagues = LM.get_list_of_leagues()
        self.leagues.sort()

        self.lega = StringVar()

        for l in self.leagues:
            r = Radiobutton(self.main_f, text = l, variable = self.lega, value = l)
            r.pack()

        b = Frame(self.main_f)

        exB = Button(b, text = "Esci", command = self.exit)
        exB.pack(side = RIGHT, pady = (20, 20), padx = (5, 10))

        okB = Button(b, text = "OK", command = self.confirm_league)
        okB.pack(side = RIGHT, pady = (20, 20))

        delB = Button(b, text = "Elimina lega", command = self.delete_league)
        delB.pack(side = RIGHT, pady = (20, 20))

        newB = Button(b, text = "Nuova lega", command = self.new_league)
        newB.pack(side = RIGHT, pady = (20, 20))

        b.pack(side=BOTTOM, fill=X)

        self.main_f.protocol("WM_DELETE_WINDOW", self.exit)
        self.set_icon(self.main_f)
        self.main_f.mainloop()

    def home_page(self):
        self.main_f = Tk()
        self.main_f.geometry("800x500+200+100")
        self.main_f.title("FM - Home Page")

        l = Label(self.main_f, text = "Lega in uso : " + self.lm.league["name"], font = ("Helvetica", 16))
        l.pack(fill = X, pady = (20, 20))

        c_clasB = Button(self.main_f, text = "Calcola punteggi", font = ("Helvetica", 12), bg = "#01A9DB", command = self.calc_turn)
        c_clasB.pack(fill = BOTH, expand = 1, pady = (0, 20), padx = (5, 10))

        s_clasB = Button(self.main_f, text = "Mostra classifiche", font = ("Helvetica", 12), bg = "#01A9DB", command = self.show_class)
        s_clasB.pack(fill = BOTH, expand = 1, pady = (0, 20), padx = (5, 10))

        s_teamB = Button(self.main_f, text = "Mostra squadre", font = ("Helvetica", 12), bg = "#01A9DB", command = self.show_teams)
        s_teamB.pack(fill = BOTH, expand = 1, pady = (0, 20), padx = (5, 10))

        i_formB = Button(self.main_f, text = "Inserisci formazione", font = ("Helvetica", 12), bg = "#01A9DB", command = self.insert_form)
        i_formB.pack(fill = BOTH, expand = 1, pady = (0, 20), padx = (5, 10))

        m_sqadB = Button(self.main_f, text = "Modifica squadra", font = ("Helvetica", 12), bg = "#01A9DB", command = self.mod_team)
        m_sqadB.pack(fill = BOTH, expand = 1, pady = (0, 20), padx = (5, 10))

        i_manaB = Button(self.main_f, text = "Inserisci manager", font = ("Helvetica", 12), bg = "#01A9DB", command = self.ins_manager)
        i_manaB.pack(fill = BOTH, expand = 1, pady = (0, 20), padx = (5, 10))

        add_peB = Button(self.main_f, text = "Aggiungi penalità", font = ("Helvetica", 12), bg = "#01A9DB", command = self.add_penality)
        add_peB.pack(fill = BOTH, expand = 1, pady = (0, 20), padx = (5, 10))

        self.main_f.protocol("WM_DELETE_WINDOW", self.exit)
        self.set_icon(self.main_f)
        self.main_f.mainloop()

    def ins_manager(self):
        self.ins_manager_f =Toplevel()
        self.ins_manager_f.geometry("400x200+400+200")
        self.ins_manager_f.title("FM - Inserisci nuovo manager")

        l = Label(self.ins_manager_f, text = "Inserisci il nome del nuovo manager", font=("Helvetica", 16))
        l.pack(fill = X, pady = (20, 20))

        self.n = Entry(self.ins_manager_f)
        self.n.focus()
        self.n.pack(fill = X)

        bn = Frame(self.ins_manager_f)
        insertB = Button(bn, text = "Inserisci", command = self.insert_new_man)
        insertB.pack(side = RIGHT, pady = (20, 20), padx = (10 ,10))
        bn.pack(side=BOTTOM, fill=X)
        
        self.ins_manager_f.focus_force()
        self.set_icon(self.ins_manager_f)
        self.ins_manager_f.mainloop()

    def insert_new_man(self):
        r = self.lm.add_manager(self.n.get())
        if r == 2:
            messagebox.showinfo(title = "FM - Info", message = self.n.get() + " inserito nel database.")
            self.ins_manager_f.destroy()
        elif r == 1:
            messagebox.showwarning(title = "FM - Errore", message = "Il nome del manager non può essere vuoto")
            self.ins_manager_f.destroy()
        elif r == 0:
            messagebox.showwarning(title = "FM - Errore", message = "Il nome del manager è già utilizzato.")
            self.ins_manager_f.destroy()

    def mod_team(self):
        self.mod_team1_f = Toplevel()
        self.mod_team1_f.geometry("800x400+200+100")
        self.mod_team1_f.title("FM - Selezione manager")

        l = Label(self.mod_team1_f, text = "Seleziona il manager di cui modificare la squadra", font=("Helvetica", 16))
        l.pack(fill = X, pady = (20, 20))

        man = [m for m in self.lm.league["allenatori"].keys()]
        man.sort()

        self.manager = StringVar()

        for m in man:
            r = Radiobutton(self.mod_team1_f, text = m, variable = self.manager, value = m)
            r.pack()

        b = Frame(self.mod_team1_f)

        exB = Button(b, text = "Esci", command = lambda: self.mod_team1_f.destroy())
        exB.pack(side = RIGHT, pady = (20, 20), padx = (5, 10))

        okB = Button(b, text = "OK", command = self.mod_team2)
        okB.pack(side = RIGHT, pady = (20, 20))

        b.pack(side=BOTTOM, fill=X)

        self.set_icon(self.mod_team1_f)
        self.mod_team1_f.mainloop()

    def mod_team2(self):
        if self.manager.get() == "":
            messagebox.showwarning(title = "FM - Errore", message = "Nessun manager selezionato")
            self.mod_team1_f.destroy()
            self.mod_team()            
        else:
            self.mod_team1_f.destroy()
            self.t_list = [("n_portieri", "Portiere"), ("n_difensori", "Difensore"), ("n_centrocampisti", "Centrocampista"), ("n_attaccanti", "Attaccante")]
            self.inserted_players = []
            self.select_players()

    def select_players(self):
        self.dict_stat   = StatDownloader().load_stat()
        players = [str(p) for p in self.dict_stat if self.dict_stat[p]["ruolo"] == self.t_list[0][1]]

        n_play = self.lm.league[self.t_list[0][0]]
        self.select_players_f = Toplevel()
        self.select_players_f.title("FM - Selezione giocatori")
        self.select_players_f.geometry("600x" + str(n_play * 25 + 120) + "+300+100")

        l = Label(self.select_players_f, text = "Seleziona i giocatori della squadra", font=("Helvetica", 16))
        l.grid(row = 0, columnspan = 4, pady = 15)

        if len(self.lm.league["allenatori"][self.manager.get()]["giocatori"].keys()) > 0:
            player_d = [str(p) for p in self.lm.league["allenatori"][self.manager.get()]["giocatori"] if self.lm.league["allenatori"][self.manager.get()]["giocatori"][p]["ruolo"] == self.t_list[0][1]]
            self.entries = [AutocompleteEntry(players, self.select_players_f, i) for i in player_d]
            self.costs = [StringVar() for i in player_d]
            for i in range(n_play):
                self.costs[i].set(self.lm.league["allenatori"][self.manager.get()]["giocatori"][player_d[i]]["costo"])
            self.costs_s = [Spinbox(self.select_players_f, from_ = 1, to = 1000, textvariable = self.costs[i]) for i in range(n_play)]

        else:
            self.entries = [AutocompleteEntry(players, self.select_players_f, "") for i in range(n_play)]
            self.costs = [StringVar() for i in range(n_play)]
            self.costs_s = [Spinbox(self.select_players_f, from_ = 1, to = 1000, textvariable = self.costs[i]) for i in range(n_play)]
        
        for e in range(n_play):
            l1 = Label(self.select_players_f, text = "Nome: ", font=("Helvetica"))
            l2 = Label(self.select_players_f, text = "Costo: ", font=("Helvetica"))
            l1.grid(row = e + 1, column = 0, padx = 10)
            self.entries[e].grid(row = e + 1, column = 1, padx = 10)
            l2.grid(row = e + 1, column = 2, padx = 10)
            self.costs_s[e].grid(row = e + 1, column = 3, padx = 10)
        
        b = Frame(self.select_players_f)

        okB = Button(b, text = "OK", command = self.validate_players)
        okB.pack(side = RIGHT, pady = (20, 20), padx = (20, 20))

        b.grid(row = n_play + 1, column = 4)
        self.set_icon(self.select_players_f)
        self.select_players_f.mainloop()

    def validate_players(self):
        players = [str(p) for p in self.dict_stat if self.dict_stat[p]["ruolo"] == self.t_list[0][1]]    
        players_set = set()

        for e in self.entries:
            if e.get() in players and e.get() != "":
                players_set.add(e.get())
        
        if len(players_set) != self.lm.league[self.t_list[0][0]]:
            messagebox.showwarning(title = "FM - Errore", message = "Giocatori non inseriti in modo corretto")
            self.select_players_f.destroy()
            self.select_por()

        else:
            for i in range(len(self.entries)):
                self.inserted_players.append((self.entries[i].get(), self.t_list[0][1], int(self.costs[i].get())))

            self.select_players_f.destroy()
            self.t_list.pop(0)
            if len(self.t_list) > 0:
                self.select_players()
            else:
                self.lm.reset_players(self.manager.get())
                for p in self.inserted_players:
                    self.lm.add_player(self.manager.get(), p[0], p[1], p[2])

                messagebox.showinfo(title = "FM - Info", message = "Squadra inserita correttamente nel database.")

    def insert_form(self):
        self.insert_form1_f = Toplevel()
        self.insert_form1_f.geometry("800x400+200+100")
        self.insert_form1_f.title("FM - Selezione manager")

        l = Label(self.insert_form1_f, text = "Seleziona il manager di cui inserire la formazione", font=("Helvetica", 16))
        l.pack(fill = X, pady = (20, 20))

        man = [m for m in self.lm.league["allenatori"].keys()]
        man.sort()

        self.manager = StringVar()
        self.manager.set("")

        for m in man:
            r = Radiobutton(self.insert_form1_f, text = m, variable = self.manager, value = m)
            r.pack()

        b = Frame(self.insert_form1_f)

        exB = Button(b, text = "Esci", command = lambda: self.insert_form1_f.destroy())
        exB.pack(side = RIGHT, pady = (20, 20), padx = (5, 10))

        okB = Button(b, text = "OK", command = self.insert_form2)
        okB.pack(side = RIGHT, pady = (20, 20))

        b.pack(side=BOTTOM, fill=X)

        self.set_icon(self.insert_form1_f)
        self.insert_form1_f.mainloop()

    def insert_form2(self):
        if self.manager.get() == "":
            messagebox.showwarning(title = "FM - Errore", message = "Nessun manager selezionato")
            self.insert_form1_f.destroy()
            self.insert_form()            
        else:
            self.insert_form1_f.destroy()
            self.select_turn()

    def select_turn(self):
        self.select_turn_f =Toplevel()
        self.select_turn_f.geometry("400x200+400+200")
        self.select_turn_f.title("FM - Selezione giornata")

        l = Label(self.select_turn_f, text = "Seleziona la giornata", font=("Helvetica", 16))
        l.pack(fill = X, pady = (20, 20))

        self.turn = StringVar()
        self.turn_s = Spinbox(self.select_turn_f, from_ = 1, to = 38, textvariable = self.turn)
        self.turn_s.pack()

        b = Frame(self.select_turn_f)

        def ind():
            self.select_turn_f.destroy()
            self.insert_form()

        inB = Button(b, text = "Indietro", command = ind)
        inB.pack(side = RIGHT, pady = (20, 20), padx = (0, 20))

        okB = Button(b, text = "OK", command = self.select_mod)
        okB.pack(side = RIGHT, pady = (20, 20), padx = (20, 20))

        b.pack(side = BOTTOM, fill = X)
        self.set_icon(self.select_turn_f)
        self.select_turn_f.mainloop()

    def select_mod(self):
        self.select_turn_f.destroy()
        self.select_mod_f = Toplevel()
        self.select_mod_f.geometry("800x400+200+100")
        self.select_mod_f.title("FM - Selezione modulo")

        l = Label(self.select_mod_f, text = "Seleziona il modulo da utilizzare in questa giornata", font=("Helvetica", 16))
        l.pack(fill = X, pady = (20, 20))

        self.modulo = StringVar()
        self.modulo.set("")

        moduli = ["3-4-3", "3-5-2", "4-3-3", "4-4-2", "4-5-1", "5-3-2", "5-4-1"]

        for m in moduli:
            r = Radiobutton(self.select_mod_f, text = m, variable = self.modulo, value = m)
            r.pack()

        b = Frame(self.select_mod_f)

        def ind():
            self.select_mod_f.destroy()
            self.select_turn()

        inB = Button(b, text = "Indietro", command = ind)
        inB.pack(side = RIGHT, pady = (20, 20), padx = (0, 20))

        okB = Button(b, text = "OK", command = self.select_mod2)
        okB.pack(side = RIGHT, pady = (20, 20))

        b.pack(side=BOTTOM, fill=X)

        self.set_icon(self.select_mod_f)
        self.select_mod_f.mainloop()

    def select_mod2(self):
        mod = self.modulo.get()
        if mod == "":
            messagebox.showwarning(title = "FM - Errore", message = "Nessun modulo selezionato")
            self.select_mod_f.destroy()
            self.select_mod()            
        else:
            self.select_mod_f.destroy()
            self.insert_players(int(mod[0]), int(mod[2]), int(mod[4]))

    def insert_players(self, n_dif, n_cen, n_att):
        players = self.lm.league["allenatori"][self.manager.get()]["giocatori"]
        portieri = [n for n in players if players[n]["ruolo"] == "Portiere"]        
        difensori = [n for n in players if players[n]["ruolo"] == "Difensore"]
        centrocampisti = [n for n in players if players[n]["ruolo"] == "Centrocampista"]
        attaccanti = [n for n in players if players[n]["ruolo"] == "Attaccante"]

        self.insert_players_f = Toplevel()
        self.insert_players_f.title("FM - Inserimento formazione")
        self.insert_players_f.geometry("400x800+400+10")

        l = Label(self.insert_players_f, text = "Seleziona i titolari di giornata", font=("Helvetica", 14))
        l.grid(row = 0, columnspan = 2, pady = 15)

        self.por_t = AutocompleteEntry(portieri, self.insert_players_f, "")
        self.dif_t = [AutocompleteEntry(difensori, self.insert_players_f, "") for i in range(n_dif)]
        self.cen_t = [AutocompleteEntry(centrocampisti, self.insert_players_f, "") for i in range(n_cen)]
        self.att_t = [AutocompleteEntry(attaccanti, self.insert_players_f, "") for i in range(n_att)]
        self.por_p = [AutocompleteEntry(portieri, self.insert_players_f, "") for i in range(2)]
        self.dif_p = [AutocompleteEntry(difensori, self.insert_players_f, "") for i in range(3)]
        self.cen_p = [AutocompleteEntry(centrocampisti, self.insert_players_f, "") for i in range(3)]
        self.att_p = [AutocompleteEntry(attaccanti, self.insert_players_f, "") for i in range(2)]
              
        l = Label(self.insert_players_f, text = "Portiere: ", font=("Helvetica"))
        l.grid(row = 1, column = 0, padx = 10)
        self.por_t.grid(row = 1, column = 1, padx = 10)

        row = 2

        for e in range(n_dif):
            l = Label(self.insert_players_f, text = "Difensore: ", font=("Helvetica"))
            l.grid(row = row, column = 0, padx = 10)
            self.dif_t[e].grid(row = row, column = 1, padx = 10)
            row = row + 1

        for e in range(n_cen):
            l = Label(self.insert_players_f, text = "Centrocampista: ", font=("Helvetica"))
            l.grid(row = row, column = 0, padx = 10)
            self.cen_t[e].grid(row = row, column = 1, padx = 10)
            row = row + 1

        for e in range(n_att):
            l = Label(self.insert_players_f, text = "Attaccante: ", font=("Helvetica"))
            l.grid(row = row, column = 0, padx = 10)
            self.att_t[e].grid(row = row, column = 1, padx = 10)
            row = row + 1

        l = Label(self.insert_players_f, text = "Seleziona la panchina di giornata", font=("Helvetica", 14))
        l.grid(row = row, columnspan = 2, pady = 15)
        row = row + 1

        for e in range(2):
            l = Label(self.insert_players_f, text = "Portiere: ", font=("Helvetica"))
            l.grid(row = row, column = 0, padx = 10)
            self.por_p[e].grid(row = row, column = 1, padx = 10)
            row = row + 1

        for e in range(3):
            l = Label(self.insert_players_f, text = "Difensore: ", font=("Helvetica"))
            l.grid(row = row, column = 0, padx = 10)
            self.dif_p[e].grid(row = row, column = 1, padx = 10)
            row = row + 1

        for e in range(3):
            l = Label(self.insert_players_f, text = "Centrocampista: ", font=("Helvetica"))
            l.grid(row = row, column = 0, padx = 10)
            self.cen_p[e].grid(row = row, column = 1, padx = 10)
            row = row + 1

        for e in range(2):
            l = Label(self.insert_players_f, text = "Attaccante: ", font=("Helvetica"))
            l.grid(row = row, column = 0, padx = 10)
            self.att_p[e].grid(row = row, column = 1, padx = 10)
            row = row + 1

        b = Frame(self.insert_players_f)

        def ind():
            self.insert_players_f.destroy()
            self.select_mod()

        inB = Button(b, text = "Indietro", command = ind)
        inB.pack(side = RIGHT, pady = (20, 20), padx = (0, 20))

        okB = Button(b, text = "OK", command = self.validate_form)
        okB.pack(side = RIGHT, pady = (20, 20), padx = (20, 20))

        b.grid(row = row , column = 1)
        self.set_icon(self.insert_players_f)
        self.insert_players_f.mainloop()


    def validate_form(self):
        players = self.lm.league["allenatori"][self.manager.get()]["giocatori"]
        portieri = [n for n in players if players[n]["ruolo"] == "Portiere"]        
        difensori = [n for n in players if players[n]["ruolo"] == "Difensore"]
        centrocampisti = [n for n in players if players[n]["ruolo"] == "Centrocampista"]
        attaccanti = [n for n in players if players[n]["ruolo"] == "Attaccante"]

        form = {}
        form["por_t"] = self.por_t.get()
        form["dif_t"] = [d.get() for d in self.dif_t] 
        form["cen_t"] = [c.get() for c in self.cen_t] 
        form["att_t"] = [a.get() for a in self.att_t]         
        form["por_p"] = [p.get() for p in self.por_p]
        form["dif_p"] = [d.get() for d in self.dif_p] 
        form["cen_p"] = [c.get() for c in self.cen_p] 
        form["att_p"] = [a.get() for a in self.att_p] 

        valid = True
        set_p = set()
        for d in form["dif_t"] + form["dif_p"]:
            if d in difensori and d != "":
                set_p.add(d)

        if len(set_p) != len(form["dif_t"] + form["dif_p"]):
            valid = False   

        set_p = set()
        for c in form["cen_t"] + form["cen_p"]:
            if c in centrocampisti and c != "":
                set_p.add(c)

        if len(set_p) != len(form["cen_t"] + form["cen_p"]):
            valid = False 

        set_p = set()
        for a in form["att_t"] + form["att_p"]:
            if a in attaccanti and a != "":
                set_p.add(a)
        
        if len(set_p) != len(form["att_t"] + form["att_p"]):
            valid = False 

        set_p = set()
        for p in form["por_p"] + [form["por_t"]]:
            if p in portieri and p != "":
                set_p.add(p)

        if len(set_p) != len(form["por_p"] + [form["por_t"]]):
            valid = False 

        if valid == True:
            messagebox.showinfo(title = "FM - Info", message = "La formazione di " + self.manager.get() + " per il turno " + self.turn.get() + " è stata inserita")
            self.insert_players_f.destroy()
            self.lm.insert_team(self.manager.get(), int(self.turn.get()), form)
        else:
            messagebox.showwarning(title = "FM - Errore", message = "Giocatori non inseriti nel modo corretto")
            self.insert_players_f.destroy()
            mod = self.modulo.get()
            self.insert_players(int(mod[0]), int(mod[2]), int(mod[4]))


    def calc_turn(self):
        self.calc_turn_f =Toplevel()
        self.calc_turn_f.geometry("400x200+400+200")
        self.calc_turn_f.title("FM - Selezione giornata")

        l = Label(self.calc_turn_f, text = "Seleziona la giornata", font=("Helvetica", 16))
        l.pack(fill = X, pady = (20, 20))

        self.turn_s = Spinbox(self.calc_turn_f, from_ = 1, to = 38)
        self.turn_s.pack()

        b = Frame(self.calc_turn_f)

        okB = Button(b, text = "OK", command = self.validate_turn)
        okB.pack(side = RIGHT, pady = (20, 20), padx = (20, 20))

        b.pack(side = BOTTOM, fill = X)
        self.set_icon(self.calc_turn_f)
        self.calc_turn_f.mainloop()

    def validate_turn(self):
        self.lm.load_league()
        if self.lm.control_turn_team(self.turn_s.get()):
            self.turn_s = self.turn_s.get()
            self.calc_turn_f.destroy()
            self.show_turn()
        else:
            messagebox.showwarning(title = "FM - Errore", message = "Le formazioni per la giornata selezionata non sono state inserite")
            self.calc_turn_f.destroy()
            self.calc_turn()

    def show_turn(self):
        self.show_turn_f =Toplevel()
        self.show_turn_f.title("FM - Risultati giornata " + self.turn_s)
        self.show_turn_f.geometry("1000x800")
        self.show_turn_f.attributes('-zoomed', True)
        res_dict = self.lm.calc_turn_score(self.turn_s)
        tree = ttk.Treeview(self.show_turn_f, height="30")
        pdf = PdfCreator("Turno " + self.turn_s + " - " + self.lm.league["name"])
 
        tree["columns"] = ("Voto", "Gol", "Assist", "Rigori seganti/parati", "Rigori sbagliati", "Autogol", "Ammonizioni", "Espulsioni", "Fantavoto")
        tree.column("Voto", width = 70)
        tree.column("Gol", width = 70)
        tree.column("Assist", width = 70)
        tree.column("Rigori seganti/parati", width = 150)
        tree.column("Rigori sbagliati", width = 120)
        tree.column("Autogol", width = 100)
        tree.column("Ammonizioni", width = 100)
        tree.column("Espulsioni", width = 100)
        tree.column("Fantavoto", width = 100)
        
        tree.heading("Voto", text="Voto")
        tree.heading("Gol", text="Gol")
        tree.heading("Assist", text="Assist")
        tree.heading("Rigori seganti/parati", text="Rigori seganti/parati")
        tree.heading("Rigori sbagliati", text="Rigori sbagliati")
        tree.heading("Autogol", text="Autogol")
        tree.heading("Ammonizioni", text="Ammonizioni")
        tree.heading("Espulsioni", text="Espulsioni")
        tree.heading("Fantavoto", text="Fantavoto")
        
        man = [k for k in res_dict.keys()]
        man.sort()

        for i in range(len(man)):
            table_data =[["Giocatore","Voto", "Gol", "Assist", "Rigori seg/par", "Rigori sba", "Autogol", "Ammonizioni", "Espulsioni", "Fantavoto"]]
            turn = self.lm.league["allenatori"][man[i]]["giornate"][str(self.turn_s)]
            tree.insert("", i, man[i], text = man[i] + " - " + str(turn["score"]))
            n = 1
            t = [0.0, 0, 0, 0, 0, 0, 0, 0]

            for p in res_dict[man[i]]:
                tree.insert(man[i], n, text = p[0], values = (p[1], p[2], p[3], p[4], p[5], p[6], p[7], p[8], p[9]))
                table_data.append([str(p[0]), str(p[1]), str(p[2]), str(p[3]), str(p[4]), str(p[5]), str(p[6]), str(p[7]), str(p[8]), str(p[9])])
                n = n + 1
                if p[1] != "-":
                    for it in range(len(t)):
                        t[it] = t[it] + p[it + 1]

            tree.insert(man[i], n, text = "Modificatore", values = ("-", "-", "-", "-", "-", "-", "-", "-", str(turn["modificatore"])))                
            table_data.append(["Modificatore", "-", "-", "-", "-", "-", "-", "-", "-", str(turn["modificatore"])])           
            tree.insert(man[i], n, text = "Totale", values = (t[0], t[1], t[2], t[3], t[4], t[5], t[6], t[7], str(turn["score"])))
            table_data.append(["Totale", str(t[0]), str(t[1]), str(t[2]), str(t[3]), str(t[4]), str(t[5]), str(t[6]), str(t[7]), str(turn["score"])])
            pdf.insert_table(man[i], table_data)
        tree.pack()


        b = Frame(self.show_turn_f)

        def export():
            pdf.create_pdf()

        okB = Button(b, text = "Esporta in PDF", command = export)
        okB.pack(side = RIGHT, pady = (20, 20), padx = (20, 20))

        b.pack(side = BOTTOM, fill = X)
        self.set_icon(self.show_turn_f)
        self.show_turn_f.mainloop()

    def show_class(self):
        self.show_class_f =Toplevel()
        self.show_class_f.title("FM - Classifica")
        self.show_class_f.geometry("1000x800")
        self.show_class_f.attributes('-zoomed', True)
        tree = ttk.Treeview(self.show_class_f, height="30")

        man = [k for k in self.lm.league["allenatori"].keys()]
        man.sort()
        tree["columns"] = man

        tot = []
        for m in man:
            tree.column(m, width = 70)
            tree.heading(m, text=m)
            tot.append(0.0)

        tree.insert("", 0, "Giornate", text = "Giornate")
        table_header = ["Giornata"]
        for m in man:
            table_header.append(m)
        table_data = [table_header]

        for i in range(1, 39):
            scores = []
            for m in man:
                if str(i) in self.lm.league["allenatori"][m]["giornate"] and "score" in self.lm.league["allenatori"][m]["giornate"][str(i)]:
                    score = self.lm.league["allenatori"][m]["giornate"][str(i)]["score"]
                    scores.append(str(score))
                    ind = man.index(m)
                    tot[ind] = tot[ind] + score
                else:
                    scores.append("-")

            tree.insert("Giornate", i, i, text = i, values = scores)
            turn = [str(i)]
            for s in scores:
                turn.append(str(s))
            table_data.append(turn)

        pen = []
        for m in man:
            p =  self.lm.league["allenatori"][m]["penalità"]
            pen.append(p)
            ind = man.index(m)
            tot[ind] = tot[ind] - p

        tree.insert("", 39, "Pen", text = "Penalità", values = pen)
        tree.insert("", 40, "Tot", text = "Totale", values = tot)
        tots = ["Totale"]
        for t in tot:
            tots.append(str(t))

        pens = ["Penalità"]
        for p in pen:
            pens.append(str(p))

        table_data.append(pens)
        table_data.append(tots)
        tree.pack()

        b = Frame(self.show_class_f)

        def export():
            pdf = PdfCreator("Classifica - " + self.lm.league["name"])
            pdf.insert_table("Classifica", table_data)
            pdf.create_pdf()

        okB = Button(b, text = "Esporta in PDF", command = export)
        okB.pack(side = RIGHT, pady = (20, 20), padx = (20, 20))

        b.pack(side = BOTTOM, fill = X)
        self.set_icon(self.show_class_f)
        self.show_class_f.mainloop()

    def add_penality(self):
        self.add_penality1_f = Toplevel()
        self.add_penality1_f.geometry("800x400+200+100")
        self.add_penality1_f.title("FM - Selezione manager")

        l = Label(self.add_penality1_f, text = "Seleziona il manager a cui attribuire una penalità", font=("Helvetica", 16))
        l.pack(fill = X, pady = (20, 20))

        man = [m for m in self.lm.league["allenatori"].keys()]
        man.sort()

        self.manager = StringVar()
        self.manager.set("")

        for m in man:
            r = Radiobutton(self.add_penality1_f, text = m, variable = self.manager, value = m)
            r.pack()

        b = Frame(self.add_penality1_f)

        exB = Button(b, text = "Esci", command = lambda: self.add_penality1_f.destroy())
        exB.pack(side = RIGHT, pady = (20, 20), padx = (5, 10))

        okB = Button(b, text = "OK", command = self.add_penality2)
        okB.pack(side = RIGHT, pady = (20, 20))

        b.pack(side=BOTTOM, fill=X)

        self.set_icon(self.add_penality1_f)
        self.add_penality1_f.mainloop()

    def add_penality2(self):
        if self.manager.get() == "":
            messagebox.showwarning(title = "FM - Errore", message = "Nessun manager selezionato")
            self.add_penality1_f.destroy()
            self.add_penality()            
        else:
            self.add_penality1_f.destroy()
            self.select_entity()

    def select_entity(self):
        self.select_entity_f =Toplevel()
        self.select_entity_f.geometry("400x200+400+200")
        self.select_entity_f.title("FM - Selezione penalità")

        l = Label(self.select_entity_f, text = "Seleziona l'entità della penalità'", font=("Helvetica", 16))
        l.pack(fill = X, pady = (20, 20))

        self.entity = StringVar()
        self.entity_s = Spinbox(self.select_entity_f, from_ = 0, to = 38, textvariable = self.entity, increment = 0.5)
        self.entity_s.pack()

        b = Frame(self.select_entity_f)

        def ind():
            self.select_entity_f.destroy()
            self.add_penality()

        inB = Button(b, text = "Indietro", command = ind)
        inB.pack(side = RIGHT, pady = (20, 20), padx = (0, 20))

        okB = Button(b, text = "OK", command = self.apply_penality)
        okB.pack(side = RIGHT, pady = (20, 20), padx = (20, 20))

        b.pack(side = BOTTOM, fill = X)
        self.set_icon(self.select_entity_f)
        self.select_entity_f.mainloop()

    def apply_penality(self):
        a = messagebox.askyesno(title = "FM penalità", message = "Vuoi veramente applicare una penalità di " + self.entity.get() + " punti a " + self.manager.get())
        if a:
            self.lm.apply_penality(self.manager.get(), float(self.entity.get()))
            messagebox.showinfo(title = "FM - Info", message = "Penalità applicata.")
            self.select_entity_f.destroy()
        else:
            messagebox.showinfo(title = "FM - Info", message = "Penalità non applicata.")
            self.select_entity_f.destroy()    

    def show_teams(self):
        self.show_teams_f =Toplevel()
        self.show_teams_f.title("FM - Squadre del campionato")
        self.show_teams_f.geometry("1000x800")
        self.show_teams_f.attributes('-zoomed', True)
        tree = ttk.Treeview(self.show_teams_f, height="30")
        pdf = PdfCreator("Squadre - " + self.lm.league["name"])
 
        tree["columns"] = ("Giocatore", "Ruolo", "Prezzo pagato")
        tree.column("Giocatore", width = 150)
        tree.column("Ruolo", width = 70)
        tree.column("Prezzo pagato", width = 100)
        
        tree.heading("Giocatore", text="Giocatore")
        tree.heading("Ruolo", text="Ruolo")
        tree.heading("Prezzo pagato", text="Prezzo pagato")
        
        man = [k for k in self.lm.league["allenatori"].keys()]
        man.sort()
        n = 1

        for m in man:
            table_data =[["Giocatore", "Ruolo", "Prezzo pagato"]]
            players = self.lm.league["allenatori"][m]["giocatori"]
            tree.insert("", n, m, text = m)
            P = []
            D = []
            C = []
            A = []

            for p in players.keys():
                if players[p]["ruolo"] == "Portiere":
                    P.append(p)
                elif players[p]["ruolo"] == "Difensore":
                    D.append(p)
                elif players[p]["ruolo"] == "Centrocampista":
                    C.append(p)
                elif players[p]["ruolo"] == "Attaccante":
                    A.append(p)

            P.sort()
            D.sort()
            C.sort()
            A.sort()
            tot = 0.0
            for p in P + D + C + A:
                tree.insert(m, n, text = p, values = (players[p]["ruolo"], players[p]["costo"]))
                table_data.append([str(p), str(players[p]["ruolo"]), str(players[p]["costo"])])
                tot = tot + players[p]["costo"]
                n = n + 1

            tree.insert(m, n, text = "Totale", values = ("-", tot))
            table_data.append(["Totale", "-", str(tot)])
            pdf.insert_table(m, table_data)
            n = n + 1

        tree.pack()


        b = Frame(self.show_teams_f)

        def export():
            pdf.create_pdf()

        okB = Button(b, text = "Esporta in PDF", command = export)
        okB.pack(side = RIGHT, pady = (20, 20), padx = (20, 20))

        b.pack(side = BOTTOM, fill = X)
        self.set_icon(self.show_teams_f)
        self.show_teams_f.mainloop()



FM = FantaManager()
