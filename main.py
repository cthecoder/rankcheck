#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import sys
import time
import threading

from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import *

from check_rank_data import RetrieveData
import xmlHandler
import logFileHandler
import qmessagebox
from dialogs.optionsDialog import OptionsDialog
from dialogs.showDataWindow import DataWindow
from dialogs.manageBooks import ManageBooks


class Main(QtWidgets.QMainWindow):
	def __init__(self):
		QtWidgets.QMainWindow.__init__(self)
		self.listheader = ["Autor", "Titel", "Format", "Rank Bücher", "Rank Belletristik", "Lieferstatus"]
		self.listChanged = False
		self.connected_to_net = False
		self.checkInterval = 1
		self.added_removed = 0
		self.rowsInList = 0
		self.selectedRow = 0
		self.booklist = []
		self.bookrank = []
		self.bookfiles = []

		self.createMenuBar()
		self.createComponents()
		self.createLayout()
		self.createConnects()

		self.checkStatus()
		self.checkInternetConnection()

		self.setWindowTitle(self.tr('Amazon RankChecker'))

	def checkStatus(self):
		filelist = os.listdir('data')
		if 'books.xml' in filelist:
			try:
				xmlbooklist = xmlHandler.read("data/books.xml")
			except:
				qmessagebox.warning(self, u'books.xml ungültig. Neue Bücher anlegen.')
		else:
			startup = ManageBooks()
			startup.exec()
		self.readBookData()

	def createMenuBar(self):
		# MenuItems
		self.actionAbout = QtWidgets.QAction(self.tr("Über das Programm"), self)
		self.actionHelp = QtWidgets.QAction(self.tr("Kurze Anleitung"), self)
		menuInfo = self.menuBar().addMenu(self.tr("Info"))
		menuInfo.addAction(self.actionAbout)
		menuInfo.addAction(self.actionHelp)

		self.actionOptions = QtWidgets.QAction(self.tr("Optionen"), self)
		self.actionAdminBooks = QtWidgets.QAction(self.tr("Bücher verwalten"), self)
		menuEinstellungen = self.menuBar().addMenu(self.tr("Einstellungen"))
		menuEinstellungen.addAction(self.actionAdminBooks)
		menuEinstellungen.addAction(self.actionOptions)  # Triggers
		self.actionAdminBooks.triggered.connect(self.showManageBooks)
		self.actionOptions.triggered.connect(self.showOptions)

	def createComponents(self):

		self.infoLine = QtWidgets.QLabel(u'Auch kein Interesse an Amazon-Ranks? Dann den Computer nachsehenlassen!')
		self.infoLine.setAlignment(Qt.AlignLeft)
		self.progBar = QtWidgets.QProgressBar()
		self.progBar.setTextVisible(False)
		self.progBar.setFixedHeight(10)

		self.linie1 = QtWidgets.QFrame()
		# self.linie1.setMinimumSize(350, 1)
		self.linie1.setFrameShape(QtWidgets.QFrame.HLine)
		self.linie1.setFrameShadow(QtWidgets.QFrame.Sunken)

		self.tabelle = QtWidgets.QTableWidget()
		self.tabelle.setContextMenuPolicy(Qt.CustomContextMenu)
		self.tabelle.customContextMenuRequested.connect(self.showRankData)
		self.tabelle.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)  # schaltet Editier-Möglichkeit der
		# Zellen aus
		self.tabelle.setColumnCount(6)  # auf variable umstellen
		self.tabelle.setHorizontalHeaderLabels(self.listheader)
		self.tabelle.verticalHeader().setVisible(False)
		self.tabelle.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
		self.tabelle.cellDoubleClicked.connect(self.showRankData)

		# TODO handling wenn mehr als 10 titel oder so:
		# self.tabelle.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)

		self.btn_up = QtWidgets.QPushButton(u'Up')
		self.btn_down = QtWidgets.QPushButton(u'Down')
		self.btn_exit = QtWidgets.QPushButton(u"Beenden")
		self.btn_update = QtWidgets.QPushButton(u"Aktualisieren")
		self.btn_saveData = QtWidgets.QPushButton("Speichern")
		self.btn_saveData.setEnabled(False)
		self.statusleiste = QtWidgets.QStatusBar(self)

	def createLayout(self):
		self.layoutzentral = QtWidgets.QVBoxLayout()
		widgetzentral = QtWidgets.QWidget()
		widgetzentral.setLayout(self.layoutzentral)
		self.setCentralWidget(widgetzentral)

		self.layoutzentral.addWidget(self.infoLine)
		self.layoutzentral.addWidget(self.progBar)
		self.layoutzentral.addWidget(self.linie1)
		self.layoutzentral.addWidget(self.linie1)

		self.table_ly = QtWidgets.QHBoxLayout()

		buttonUpDown_ly = QtWidgets.QVBoxLayout()
		buttonUpDown_ly.addWidget(self.btn_up)
		buttonUpDown_ly.addWidget(self.btn_down)

		buttonUpDown_ly.setAlignment(Qt.AlignTop)  # setAligment > nur mit Layout-Objekten
		self.table_ly.addLayout(buttonUpDown_ly, stretch = 0)
		self.table_ly.addWidget(self.tabelle, stretch = 0)

		buttons_ly = QtWidgets.QHBoxLayout()
		buttons_ly.addWidget(self.btn_update)
		buttons_ly.addWidget(self.btn_saveData)
		buttons_ly.addWidget(self.btn_exit)

		self.layoutzentral.addLayout(self.table_ly)
		self.layoutzentral.addLayout(buttons_ly)
		self.layoutzentral.addWidget(self.statusleiste)

	def createConnects(self):
		self.btn_update.clicked.connect(self.getRankData)
		self.btn_saveData.clicked.connect(self.saveRankData)
		self.btn_exit.clicked.connect(self.exitProgram)
		self.btn_up.clicked.connect(self.moveUp)
		self.btn_down.clicked.connect(self.moveDown)

	def readBookData(self):
		self.booklist = xmlHandler.read("data/books.xml")  # Liste von Listen der Buchtitel aus dem XML
		for title in self.booklist:
			filename = (title[1] + "_" + title[2] + ".csv").replace(" ", "_")  # Das_Sandkorn_Taschenbuch.csv
			self.bookfiles.append(filename)
		self.populateTable()

	def populateTable(self):  # besetzt die Tabelle mit Werten

		if self.listChanged:  # falls die Bücherliste verändert wurde: löschen/hinzufügen von Tabellenzeilen
			self.add_removeRows()

		for i in range(len(self.booklist)):  # Befüllen der Tabelle
			if not self.listChanged:  # beim ersten Aufbau der Tabelle ist listChanged = False
				self.tabelle.insertRow(i)
			author = QtWidgets.QTableWidgetItem(self.booklist[i][0])
			title = QtWidgets.QTableWidgetItem(self.booklist[i][1])
			bookformat = QtWidgets.QTableWidgetItem(self.booklist[i][2])

			self.tabelle.setItem(i, 0, author)
			self.tabelle.setItem(i, 1, title)
			self.tabelle.setItem(i, 2, bookformat)

		self.rowsInList = self.tabelle.rowCount()

		# Anpassung des Tabellenrahmens und des Fensters an die Größe der Tabelle
		self.tabelle.resizeColumnsToContents()
		self.tabelle.resizeRowsToContents()
		width = self.tabelle.horizontalHeader().length()
		height = self.tabelle.verticalHeader().length()
		self.tabelle.resize(width, height)  # Tabelle
		# print(self.tabelle.height())
		self.resize(self.tabelle.width() + 120, (self.tabelle.height()) * 2.5)  # Mainwindow

	def add_removeRows(self):
		for i in range((abs(self.added_removed))):
			if self.added_removed < 0:
				self.tabelle.removeRow(self.rowsInList - (i + 1))
			else:
				self.tabelle.insertRow(self.rowsInList + i)
		self.rowsInList = self.tabelle.rowCount()

	#     code von: http://stackoverflow.com/questions/9166087/move-row-up-and-down-in-pyqt4
	def moveUp(self):
		row = self.tabelle.currentRow()
		column = self.tabelle.currentColumn()
		if row > 0:
			self.tabelle.insertRow(row - 1)
			for i in range(self.tabelle.columnCount()):
				self.tabelle.setItem(row - 1, i, self.tabelle.takeItem(row + 1, i))
				self.tabelle.setCurrentCell(row - 1, column)
			self.tabelle.removeRow(row + 1)

	def moveDown(self):
		row = self.tabelle.currentRow()
		print('moving', self.booklist[row], ' down', row)
		column = self.tabelle.currentColumn()
		if row < self.tabelle.rowCount() - 1:
			self.tabelle.insertRow(row + 2)
			for i in range(self.tabelle.columnCount()):
				self.tabelle.setItem(row + 2, i, self.tabelle.takeItem(row, i))
				self.tabelle.setCurrentCell(row + 2, column)
			self.tabelle.removeRow(row)

	def getRankData(self):
		self.bookrank = []
		val = 0
		self.progBar.setValue(val)
		self.statusleiste.showMessage('Amazon Rank-Abfrage läuft ...')
		self.timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
		infotext = u'Letzte Abfrage: ' + self.timestamp
		self.infoLine.setText(infotext)
		bookdata = RetrieveData()
		val_incr = 100 / len(self.booklist)
		self.btn_update.setEnabled(False)
		for i in range(len(self.booklist)):
			rankdata = bookdata.get_rank(self.booklist[i][3])  # Abfrage mit Link
			if rankdata[0] == "-":  # bei Error return
				fail = QtWidgets.QTableWidgetItem(str(rankdata[0]))
				self.tabelle.setItem(i, 3, fail)
			rank = QtWidgets.QTableWidgetItem(str(rankdata[1]))
			self.tabelle.setItem(i, 3, rank)
			rank_belletristik = QtWidgets.QTableWidgetItem(str(rankdata[2]))
			self.tabelle.setItem(i, 4, rank_belletristik)
			if self.booklist[i][2] == "E-Book":
				availability = QtWidgets.QTableWidgetItem("n/a")
			else:
				availability = QtWidgets.QTableWidgetItem(str(rankdata[0]))
			self.tabelle.setItem(i, 5, availability)
			self.bookrank.append([self.timestamp, str(rankdata[1]), str(rankdata[2]), rankdata[0]])
			val += val_incr
			self.progBar.setValue(val)

		self.btn_update.setEnabled(True)
		self.btn_saveData.setEnabled(True)
		self.statusleiste.showMessage('Abfrage beendet')

	def showRankData(self, row, column):
		print("Row %d and Column %d was clicked" % (row, column))
		buchdatei = self.bookfiles[row]
		datawindow = DataWindow(buchdatei)
		self.selectedRow = self.tabelle.currentRow()  # index der reihe
		#     print("currow", currentrow)
		self.tabelle.selectRow(self.selectedRow)
		datawindow.exec()

	def saveRankData(self):
		for i in range(len(self.booklist)):
			csvlist = ", ".join(self.bookrank[i])
			logFileHandler.write(self.bookfiles[i], csvlist)
		self.statusleiste.showMessage('Daten gespeichert.')
		self.btn_saveData.setEnabled(False)

	def loadData(self, row, column):
		print('DOUBLEKLIK', row, column)

	def showManageBooks(self):
		book_management = ManageBooks()
		book_management.exec()
		self.listChanged = book_management.changeToList  # Bool True False
		self.added_removed = book_management.added_removed  # int +/-

		if self.listChanged:
			self.statusleiste.showMessage('Liste erweitert/verkürzt')
			self.booklist = []
			self.tabelle.clearContents()
			self.readBookData()
		else:
			self.statusleiste.showMessage('Keine Änderungen an der Liste')

	def showOptions(self):
		optionsDialog = OptionsDialog()
		optionsDialog.exec()
		if optionsDialog.autoCheckOn:
			self.checkInterval = optionsDialog.check_intervall
			self.statusleiste.showMessage('Umgestellt auf automatische Abfrage alle '+ str(self.checkInterval) +
		                              ' Stunden(n)' )
			self.runIntervalChecks()
		else:
			self.statusleiste.showMessage(u'Manuelle Abfrage')
		print('main', self.checkInterval)

	def runIntervalChecks(self):
		if self.connected_to_net:
			if not self.checkInterval == 0:
				print('running intervall check, interval = ', self.checkInterval)
				wait = self.checkInterval * 60  #3600
				next_check_at = time.strftime("%H:%M:%S %Y-%m-%d")
				#self.statusleiste.showMessage('Online / Automatische Abfrage alle ' + str(
					#self.checkInterval) + ' Stunden(n)' )
				self.getRankData()
				self.saveRankData()
				# TODO next check calculation
				#self.infoLine.setText(u'Automatische Abfrage aktiv. Nächste Abfrage um ' + str(next_check_at))
				#self.statusleiste.showMessage('Online / Automatische Abfrage')
				(threading.Timer(wait, self.runIntervalChecks)).start()  # selbst aufrufende schleife
			else:
				#TODO how to kill timer when checktime 0
				wait = 0
				try:
					(threading.Timer(wait, self.runIntervallChecks())).finished()
				except:
					pass
		else:
			pass
			#self.statusleiste.showMessage('Offline / Automatische Abfrage alle '+ str(self.checkInterval) + ' h' )


	def checkInternetConnection(self):
		msg = RetrieveData.checkInetConn()[0]  # return values : inet conn ok or non existent
		fail = RetrieveData.checkInetConn()[1]
		if fail:
			qmessagebox.warning(self, msg)
		else:
			self.statusleiste.showMessage(msg)
			self.connected_to_net = True
		# (threading.Timer(180, self.checkInternetConnection)).start()  # selbst aufrufende schleife

	def exitProgram(self):
		self.close()  # Fenster zu / Unterschied zu Exit ? oder destroy?


class rightMouseButtonHandling(QtWidgets.QTableWidget):
	print('right MOUSE BUTTON function')

	def mouseReleaseEvent(self, event):
		print('right MOUSE BUTTON function')
		if event.button() == QtCore.Qt.RightButton:
			print("Mouse Right Button Release Detected!",
			      "Detected Mouse Right Button Release")


def main():
	app = QtWidgets.QApplication(sys.argv)
	mainwindow = Main()
	mainwindow.show()
	sys.exit(app.exec_())


if __name__ == "__main__":
	main()
