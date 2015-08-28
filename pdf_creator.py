from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, inch, landscape
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, PageBreak
from reportlab.lib.styles import getSampleStyleSheet
 
class PdfCreator():
	def __init__(self, title):
		self.doc = SimpleDocTemplate("pdf/" + title + ".pdf", pagesize=A4, rightMargin=30,leftMargin=30, topMargin=30,bottomMargin=18)
		self.doc.pagesize = landscape(A4)
		self.elements = []
		

	def insert_table(self, name, table_data):
		styles = getSampleStyleSheet()
		title = Paragraph(name, styles["Heading1"])
		self.elements.append(title)

		s = getSampleStyleSheet()
		s = s["BodyText"]
		s.wordWrap = 'CJK'
		data2 = [[Paragraph(cell, s) for cell in row] for row in table_data]
		t = Table(data2)
		t.setStyle(TableStyle([	('BACKGROUND',(0,0),(-1,0),colors.grey),
								('BACKGROUND',(0,1),(0,-1),colors.lavender),
								('BOX',(0,0),(-1,-1),1,colors.black),
								('GRID',(0,0),(-1,-1),1,colors.black)
								])) 
		self.elements.append(t)
		self.elements.append(PageBreak())
		
	def create_pdf(self):
		self.doc.build(self.elements)