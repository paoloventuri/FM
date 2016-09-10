from bs4 			import BeautifulSoup
from urllib.request import urlopen
from urllib.error 	import URLError
import json, sys, re


class TurnDownloader():
	def __init__(self, turn):
		self.turn = turn
		self.year = "2016-17"
		self.load_turn()

	def download_turn(self):
		try:
			url 		= "http://www.gazzetta.it/calcio/fantanews/voti/serie-a-" + self.year + "/giornata-" + str(self.turn)
			page 		= urlopen(url)
			data		= page.read()
			self.soup 	= BeautifulSoup(data, "html.parser")
		except URLError:
			print("Controllare connessione internet.")
			sys.exit()

	def convert_f(self, f):
		if f == "-":
			return 0.0
		else:
			return float(f)


	def convert_i(self, i):
		if i == "-":
			return 0
		else:
			return int(i)


	def parse_turn(self):
		self.download_turn()
		turn_dict 	= {}
		li 			= self.soup.find_all("li")
		for l in li:
			player_stat = []
			for div in l.find_all("div"):
				span = div.find_all("span", "playerNameIn")
				if span:
					role = div.find_all("span", "playerRole show-for-small")
					if role and self.normalize_name(span[0].text) == "Lopez D" and role[0].text == "P":
						player_stat.append("Lopez Diego")
					elif role and self.normalize_name(span[0].text) == "Miranda J" and role[0].text == "D":
						player_stat.append("Miranda Joao")
					else:
						player_stat.append(self.normalize_name(span[0].text))
			for div in l.find_all("div", "inParameter"):
				player_stat.append(div.text.strip())
			
			if len(player_stat) == 11 and player_stat[10] != "-":
				turn_dict[player_stat[0]] = {
					"voto"					: self.convert_f(player_stat[2]),
					"gol"					: self.convert_i(player_stat[3]),
					"assist" 				: self.convert_i(player_stat[4]),
					"rigori segnati/parati" : self.convert_i(player_stat[5]),
					"rigori sbagliati"		: self.convert_i(player_stat[6]),
					"autogol"				: self.convert_i(player_stat[7]),
					"ammonizioni"			: self.convert_i(player_stat[8]),
					"espulsioni"			: self.convert_i(player_stat[9]),
					"magic voto"			: self.convert_f(player_stat[10])
				}

		self.turn_dict = turn_dict
		self.save_turn(turn_dict)
		return self.turn_dict

	def add_6_politico(self, players):
		turn_dict = self.turn_dict
		for p in players:
			turn_dict[p] = {
				"voto"					: 0.0,
				"gol"					: 0,
				"assist" 				: 0,
				"rigori segnati/parati" : 0,
				"rigori sbagliati"		: 0,
				"autogol"				: 0,
				"ammonizioni"			: 0,
				"espulsioni"			: 0,
				"magic voto"			: 6.0
			}	

		self.turn_dict = turn_dict
		self.save_turn(turn_dict)

	def normalize_name(self, name):
		n = ''.join(ch for ch in name if ch.isalnum() or ch == " ")
		return n.strip()

	def load_turn(self):
		try:
			with open("json/giornata_" + str(self.turn) + ".json") as f:
				self.turn_dict = json.load(f)
		except:
			return self.parse_turn()


	def save_turn(self, turn_dict):
		with open("json/giornata_" + str(self.turn) + ".json", 'w') as f: 
			f.write(json.dumps(turn_dict))