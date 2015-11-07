#!/usr/bin/python3
# -*- coding: utf-8 -*-
__author__ = 'cp'

"""
Erfassung/Bearbeitung der Titel
"""

import sys, os

from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import *

import qmessagebox
import xmlHandler


class ManageBooks(QtWidgets.QDialog):
	def __init__(self):
		QtWidgets.QDialog.__init__(self)
		self.changeToList = False
		self.initialSetup = False
		self.booksXMLfound = False
		self.added_removed = 0

		self.booklist = []

		self.createComponents()
		self.createLayout()
		self.checkInitStatus()
		self.createConnects()

	def createComponents(self):

		self.titelliste = QComboBox()

		self.intro = QtWidgets.QLabel(u'Namen des/der Autors/Autorin eingeben')
		self.hinweis = QtWidgets.QLabel(u'Hier Titel und Amazon-Link eingeben/kopieren:')

		self.autorName = QtWidgets.QLineEdit()
		self.autorName.setPlaceholderText(u"Name")
		self.cb_keepName = QtWidgets.QCheckBox(u"behalten")
		self.cb_keepName.setToolTip(u"Anklicken, damit der Verfasser-Name stehenbleibt")

		self.titelfeld = QtWidgets.QLineEdit()
		self.titelfeld.setPlaceholderText(u'Buchtitel eingeben')
		self.urlfeld = QtWidgets.QLineEdit()
		self.urlfeld.setPlaceholderText(u'Amazon-Link')
		self.urlfeld.setToolTip(u'Hier den Amazon-Link einkopieren (empfohlene Methode). ISBN-10 (ohne die '
		                        u'Bindestriche!) geht auch, kann aber zu Fehlern führen')

		self.radiobutton_tb = QRadioButton("Taschenbuch")
		self.radiobutton_hc = QRadioButton("Hardcover")
		self.radiobutton_eb = QRadioButton("E-Book")
		self.radiobutton_eb.setEnabled(False)
		self.radiobuttonlist = (self.radiobutton_tb, self.radiobutton_hc, self.radiobutton_eb)

		self.linie1 = QtWidgets.QFrame()
		self.linie1.setMinimumSize(350, 1)
		self.linie1.setFrameShape(QtWidgets.QFrame.HLine)
		self.linie1.setFrameShadow(QtWidgets.QFrame.Sunken)

		self.linie2 = QtWidgets.QFrame()
		self.linie2.setFrameShape(QtWidgets.QFrame.HLine)
		self.linie2.setFrameShadow(QtWidgets.QFrame.Sunken)

		self.linie3 = QtWidgets.QFrame()
		self.linie3.setFrameShape(QtWidgets.QFrame.HLine)
		self.linie3.setFrameShadow(QtWidgets.QFrame.Sunken)

		self.btn_addToList = QPushButton(u'Zur Liste')
		self.btn_new = QPushButton(u'Neu')
		self.btn_exit = QtWidgets.QPushButton(u"Abbrechen")
		self.btn_save = QtWidgets.QPushButton(u"Übernehmen")
		self.btn_delete = QPushButton(u"Löschen")

	def createLayout(self):
		self.dialog_ly = QtWidgets.QVBoxLayout()

		nameFields_ly = QtWidgets.QHBoxLayout()
		nameFields_ly.addWidget(self.autorName)
		nameFields_ly.addWidget(self.cb_keepName)

		inputFields_ly = QtWidgets.QHBoxLayout()
		inputFields_ly.addWidget(self.titelfeld)
		inputFields_ly.addWidget(self.urlfeld)

		self.radiobuttons_ly = QHBoxLayout()
		self.radiobuttons_ly.addWidget(self.radiobutton_tb)
		self.radiobuttons_ly.addWidget(self.radiobutton_hc)
		self.radiobuttons_ly.addWidget(self.radiobutton_eb)

		editButtons_ly = QHBoxLayout()
		editButtons_ly.addWidget(self.btn_addToList)
		editButtons_ly.addWidget(self.btn_delete)
		editButtons_ly.addWidget((self.btn_new))

		# Exit/Cancel und Übernehmen Buttons
		buttons_ly = QtWidgets.QHBoxLayout()
		buttons_ly.addWidget(self.btn_save, 0, QtCore.Qt.AlignLeft)
		buttons_ly.addWidget(self.btn_exit, 0, QtCore.Qt.AlignRight)

		# Bau des Gesamtlayouts
		self.dialog_ly.addWidget(self.intro)
		self.dialog_ly.addLayout(nameFields_ly)
		self.dialog_ly.addWidget(self.linie1)
		self.dialog_ly.addWidget(self.hinweis)
		self.dialog_ly.addLayout(inputFields_ly)
		self.dialog_ly.addLayout(self.radiobuttons_ly)
		self.dialog_ly.addLayout(editButtons_ly)
		self.dialog_ly.addWidget(self.linie2)
		self.dialog_ly.addWidget(self.titelliste)
		self.dialog_ly.addWidget(self.linie3)

		self.dialog_ly.addLayout(buttons_ly)

		self.setLayout(self.dialog_ly)
		if not self.initialSetup:
			self.setWindowTitle(u"Titel bearbeiten")
		else:
			self.setWindowTitle(u"Titel erfassen")

	def createConnects(self):
		self.btn_addToList.clicked.connect(self.addTitleToList)
		self.btn_new.clicked.connect(self.clearFields)
		self.btn_delete.clicked.connect(self.removeTitleFromList)

		self.btn_exit.clicked.connect(self.cancelApplication)
		self.btn_save.clicked.connect(self.saveAndExit)

		if not self.initialSetup:
			self.titelliste.currentIndexChanged.connect(self.populateFields)

	def checkInitStatus(self):
		filelist = os.listdir('data')
		if 'books.xml' in filelist:
			try:
				xmlbooklist = xmlHandler.read("data/books.xml")
				self.readBookList()
				self.initialSetup = False
				self.btn_save.setEnabled(False)
				self.btn_delete.setEnabled(True)
				self.btn_addToList.setEnabled(False)
			except:
				qmessagebox.warning(self, u'books.xml ungültig. Neue Bücher anlegen.')
				self.initialSetup = True
				self.btn_save.setEnabled(False)
				self.btn_delete.setEnabled(False)
				self.btn_addToList.setEnabled(True)
		else:
			self.initialSetup = True
			self.btn_addToList.setEnabled(False)
			self.btn_new.setEnabled(False)
			self.btn_save.setEnabled(False)
			self.btn_delete.setEnabled(False)

	def checkEntries(self):
		if self.autorName.text() != "" and self.titelfeld.text() != "" and self.urlfeld.text() != "":
			self.btn_new.setEnabled(True)
			self.btn_addToList.setEnabled(True)
			self.btn_delete.setEnabled(False)
			self.btn_delete.setEnabled(False)
			return True
		else:
			qmessagebox.warning(self, u'Nicht alle Felder ausgefüllt, oder Buchformat nicht gewählt')

	def addTitleToList(self):
		if self.checkEntries():
			bformat = self.getBookFormat()
			book_id = self.cleanUpURL()
			self.ausgabe = self.autorName.text() + " | " + self.titelfeld.text() + " | " + bformat
			self.titelliste.addItem(self.ausgabe)
			self.bookdata = [self.autorName.text(), self.titelfeld.text(), bformat, book_id]
			self.booklist.append(self.bookdata)
			self.clearFields()  # resetFieldsAndButtons()
			self.btn_save.setEnabled(True)
			self.added_removed += 1

	def removeTitleFromList(self):
		idx = self.titelliste.currentIndex()
		self.titelliste.removeItem(idx)
		del self.booklist[idx]
		self.btn_save.setEnabled(True)
		self.added_removed -= 1

	def getBookFormat(self):
		bookformat = "n/a"
		for button in self.radiobuttonlist:
			if button.isChecked():
				bookformat = button.text()
		return bookformat

	def cleanUpURL(self):
		book_id = ""
		if not self.urlfeld.text().isdecimal():
			try:
				stripurl = (self.urlfeld.text().rsplit("/", 1))[0]
				book_id = stripurl.split("/", 3)[3]
				return book_id
			except:
				qmessagebox.warning(self, u"Der Link ist nicht in Ordnung/fehlt. Bitte überprüfen")
		else:
			book_id = self.urlfeld.text()
			return book_id

	def readBookList(self):
		self.booklist = []
		xmlbooklist = xmlHandler.read("data/books.xml")
		bookListLength = len(xmlbooklist)
		for i in range(bookListLength):
			author = xmlbooklist[i][0]
			title = xmlbooklist[i][1]
			format = xmlbooklist[i][2]
			url = xmlbooklist[i][3]
			self.booklist.append([author, title, format, url])
		self.populateCombox()

	def populateCombox(self):
		for book in self.booklist:
			titel = book[0] + " | " + book[1] + " | " + book[2]
			self.titelliste.addItem(titel)
		self.populateFields()

	def populateFields(self):
		idx = self.titelliste.currentIndex()
		name = self.booklist[idx][0]
		titel = self.booklist[idx][1]
		bookformat = self.booklist[idx][2]
		url = self.booklist[idx][3]
		self.autorName.setText(name)
		self.titelfeld.setText(titel)
		self.urlfeld.setText(url)
		if bookformat == "Taschenbuch":
			self.radiobutton_tb.setChecked(True)
		elif bookformat == "Hardcover":
			self.radiobutton_hc.setChecked(True)
		else:
			self.radiobutton_eb.setChecked(False)  # solange diese Option disabled ist
			self.btn_new.setEnabled(True)
			self.btn_addToList.setEnabled(False)
			self.btn_delete.setEnabled(True)

	def clearFields(self):
		if not self.cb_keepName.isChecked():
			self.autorName.clear()
		self.titelfeld.clear()
		self.urlfeld.clear()
		self.btn_new.setEnabled(True)
		self.btn_save.setEnabled(False)
		self.btn_addToList.setEnabled(True)

	def cancelApplication(self):
		self.changeToList = False
		self.close()

	def saveAndExit(self):
		xmlHandler.write(self.booklist)
		self.changeToList = True
		self.close()
