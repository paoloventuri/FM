from bs4 			import BeautifulSoup
from urllib.request import urlopen
from urllib.error 	import URLError
import json

class StatDownloader():
	def __init__(self):
		self.year = "2015-16"

	def download_stat(self):
		try:
			url 		= "http://www.gazzetta.it/calcio/fantanews/statistiche/serie-a-" + self.year
			page 		= urlopen(url)
			data		= page.read()
			self.soup 	= BeautifulSoup(data, "html.parser")
		except URLError:
			print("Controllare connessione internet.")
			sys.exit()
			
	def parse_stat(self):
		self.download_stat()
		names 	= self.get_names()
		teams	= self.get_teams()
		role	= self.get_role()
		value	= self.get_int("field-q selectedField")
		games 	= self.get_int("field-pg")
		goals	= self.get_int("field-g")
		assists = self.get_int("field-a")
		yellows	= self.get_int("field-am")
		reds	= self.get_int("field-es")
		pen_att	= self.get_int("field-rt")
		pen_ok	= self.get_int("field-r")
		pen_ko	= self.get_int("field-rs")
		pen_sav = self.get_int("field-rp")
		average	= self.get_float("field-mv") 
		magic_v	= self.get_float("field-mm")
		magic_p	= self.get_float("field-mp") 

		stat 	= {}
		for i in range(len(names)):
			stat[names[i]] = {
				"squadra"			: teams[i],
				"ruolo"				: role[i],
				"valutazione"		: value[i],
				"partite"			: games[i],
				"goal"				: goals[i],
				"assist"			: assists[i],
				"gialli"			: yellows[i],
				"rossi"				: reds[i],
				"rigori tirati"		: pen_att[i],
				"rigori segnati"	: pen_ok[i],
				"rigori sbagliati"	: pen_ko[i],
				"rigori parati"		: pen_sav[i],
				"media voto"		: average[i], 
				"media magic"		: magic_v[i],
				"punti magic"		: magic_p[i] 
			}
		self.save_stat(stat)


	def get_names(self):
		l = []
		for f in self.soup.find_all("td", "field-giocatore"):
			l.append(self.normalize_name(f.text))
		return l


	def normalize_name(self, name):
		n = ''.join(ch for ch in name if ch.isalnum() or ch == " ")
		return n.strip()


	def get_teams(self):
		l = []
		for f in self.soup.find_all("span", "hidden-team-name"):
			l.append(f.text.strip().upper())
		return l


	def get_role(self):
		l 		= []
		roles 	= {
			"P" 	: "Portiere",
			"D"		: "Difensore",
			"C"		: "Centrocampista",
			"A"		: "Attaccante",
			"T (C)" : "Centrocampista",
			"T (A)" : "Attaccante"
		}
		for f in self.soup.find_all("td", "field-ruolo"):
			l.append(roles[f.text.strip()])
		return l


	def get_int(self, field_name):
		l = []
		for f in self.soup.find_all("td", field_name):
			i = f.text.strip()
			if i == "-":
				l.append(0)
			else:
				l.append(int(i))
		return l


	def get_float(self, field_name):
		l = []
		for f in self.soup.find_all("td", field_name):
			i = f.text.strip()
			if i == "-":
				l.append(0.0)
			else:
				l.append(float(i))
		return l 


	def load_stat(self):
		try:
			with open("json/statistiche.json") as f:
				return json.load(f)
		except:
			return self.parse_stat()


	def save_stat(self, stat):
		with open("json/statistiche.json", 'w') as f: 
			f.write(json.dumps(stat))
