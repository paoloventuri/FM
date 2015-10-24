from pdf_creator        import PdfCreator
from stat_downloader    import StatDownloader


pdf = PdfCreator("Quotazioni Gazzetta")

dict_stat = StatDownloader().load_stat()

players = [(str(p), dict_stat[p]["ruolo"], str(dict_stat[p]["valutazione"]), dict_stat[p]["squadra"]) for p in dict_stat]
players.sort(key=lambda x: (x[3], x[1]))


table_data = [["Giocatore", "Ruolo", "Valutazione", "Squadra"]]
for p in players:
	table_data.append([p[0], p[1], p[2], p[3]])

pdf.insert_table("Quotazioni Gazzetta", table_data)
pdf.create_pdf()