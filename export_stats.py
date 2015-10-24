from pdf_creator        import PdfCreator
from stat_downloader    import StatDownloader


pdf = PdfCreator("Quotazioni Gazzetta")

dict_stat = StatDownloader().load_stat()

por = [str(p) for p in dict_stat if dict_stat[p]["ruolo"] == "Portiere"]
por.sort()
dif = [str(p) for p in dict_stat if dict_stat[p]["ruolo"] == "Difensore"]
dif.sort()
cen = [str(p) for p in dict_stat if dict_stat[p]["ruolo"] == "Centrocampista"]
cen.sort()
att = [str(p) for p in dict_stat if dict_stat[p]["ruolo"] == "Attaccante"]
att.sort()

table_data = [["Giocatore", "Ruolo", "Valutazione", "Squadra"]]
for p in por + dif + cen + att:
	table_data.append([p, dict_stat[p]["ruolo"], str(dict_stat[p]["valutazione"]), dict_stat[p]["squadra"]])

pdf.insert_table("Quotazioni Gazzetta", table_data)
pdf.create_pdf()