from stat_downloader 	import StatDownloader
from turn_downloader	import TurnDownloader
from os.path        	import isfile, join
from os             	import listdir, remove
import json
import distutils.util
import sys

class LeagueManager():
	def __init__(self, name):
		self.l_name = name


	def get_list_of_leagues():
		files = [f for f in listdir("json/leagues") if isfile(join("json/leagues", f))]
		return [f[:-5] for f in files if f[-5:] == ".json"]


	def delete_league(self):
		remove("json/leagues/" + str(self.l_name) + ".json")


	def create_league(self, n_por, n_dif, n_cen, n_att, mod):
		self.league = {
			"name"				: self.l_name,
			"n_portieri"		: int(n_por),
			"n_difensori"		: int(n_dif),
			"n_centrocampisti"	: int(n_cen),
			"n_attaccanti"		: int(n_att),
			"modificatore"		: mod,
			"allenatori"		: {}
		}
		self.save_league()


	def add_manager(self, n):
		if n in self.league["allenatori"]:
			return 0
		elif n == "":
			return 1
		else:
			self.league["allenatori"][n] = {
				"giocatori" : {},
				"giornate"	: {}
			}
			self.save_league()
			return 2


	def add_player(self, manager, name, role, cost):
		self.league["allenatori"][manager]["giocatori"][name] = {
																	"costo" : cost,
																	"ruolo"	: role
																	}
		self.save_league()


	def reset_players(self, manager):
		self.league["allenatori"][manager]["giocatori"] = {}
		self.save_league()


	def insert_team(self, manager, turn, form):
		self.league["allenatori"][manager]["giornate"][turn] = form
		self.save_league()


	def control_turn_team(self, turn):
		for man in self.league["allenatori"].keys():
			if str(turn) not in self.league["allenatori"][man]["giornate"].keys():
				return False
			elif not set(("por_t", "por_p", "dif_t", "dif_p", "cen_t", "cen_p", "att_t", "att_p")).issubset(set([k for k in self.league["allenatori"][man]["giornate"][str(turn)].keys()])):
				return False
		
		return True


	def calc_turn_score(self, turn):
		t = TurnDownloader(turn)
		res_dict = {}
		for man in self.league["allenatori"].keys():
			form = self.league["allenatori"][man]["giornate"][str(turn)]
			score = 0.0

			por, changes = (self.calc_roles_score([form["por_t"]], form["por_p"], t.turn_dict, 0))
			dif, changes = (self.calc_roles_score(form["dif_t"], form["dif_p"], t.turn_dict, changes))
			cen, changes = (self.calc_roles_score(form["cen_t"], form["cen_p"], t.turn_dict, changes))
			att, changes = (self.calc_roles_score(form["att_t"], form["att_p"], t.turn_dict, changes))

			score = 0.0
			for p in por + dif + cen + att:
				if p[9] is not "-":
					score = score + p[9]

			if len(form["dif_t"]) > 3 and self.league["modificatore"] is True:
				mod = self.calc_mod(por, dif)
				self.league["allenatori"][man]["giornate"][str(turn)]["modificatore"] = mod
				score = score + mod
			else:
				self.league["allenatori"][man]["giornate"][str(turn)]["modificatore"] = 0.0

			self.league["allenatori"][man]["giornate"][str(turn)]["score"] = score
			res_dict[man] = por + dif + cen + att

		self.save_league()
		return res_dict


	def calc_mod(self, por, dif):
		mod = [d[1] for d in dif if d[1] != "-"]

		mod.sort(reverse = True)

		cont = False
		for p in por:
			if p[1] != "-":
				mod.insert(0, p[1])
				cont = True			

		if cont != True:
			mod.insert(0, 0.0)

		s = 0.0
		while len(mod) < 4:
			mod.append(0.0)

		for p in range(4):
			s = s + mod[p]

		s = s / 4.0
		if s >= 7.0:
			return 6.0
		elif s >= 6.5:
			return 3.0
		elif s >= 6.0:
			return 1.0
		else:
			return 0.0


	def calc_roles_score(self, tit, pan, turn_dict, changes):
		n = len(tit)
		players = []
		i = 0
		for p in tit:
			if p in turn_dict:
				i = i + 1
				d = turn_dict[p]
				players.append((p, d["voto"], d["gol"], d["assist"], d["rigori segnati/parati"], d["rigori sbagliati"], d["autogol"], d["ammonizioni"], d["espulsioni"], d["magic voto"]))
			
			else:
				players.append((p, "-", "-", "-", "-", "-", "-", "-", "-", "-", "-"))

		for p in pan:
			if p in turn_dict and i < n and changes < 3:
				changes = changes + 1
				i = i + 1
				d = turn_dict[p]
				players.append((p, d["voto"], d["gol"], d["assist"], d["rigori segnati/parati"], d["rigori sbagliati"], d["autogol"], d["ammonizioni"], d["espulsioni"], d["magic voto"]))
			
			else:
				players.append((p, "-", "-", "-", "-", "-", "-", "-", "-", "-", "-"))

		return players, changes


	def load_league(self):
		with open("json/leagues/" + str(self.l_name) + ".json") as f:
			self.league =  json.load(f)


	def save_league(self):
		with open("json/leagues/" + str(self.l_name) + ".json", 'w') as f: 
			f.write(json.dumps(self.league))