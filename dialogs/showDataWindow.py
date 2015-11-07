#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'cp'


from PyQt5 import QtWidgets
import logFileHandler


class DataWindow(QtWidgets.QDialog):

	def __init__(self, datei):
		QtWidgets.QDialog.__init__(self)
		self.datei = datei

		self.createComponents()
		self.createLayout()
		self.createConnects()
		self.processData()

	def createComponents(self):
		self.textarea = QtWidgets.QTextBrowser()
		#self.textarea = QtWidgets.QListWidget()
		self.btn_close = QtWidgets.QPushButton(u'Schließen')

	def createLayout(self):
		self.dialog_ly = QtWidgets.QVBoxLayout()
		self.dialog_ly.addWidget(self.textarea)
		self.dialog_ly.addWidget(self.btn_close)

		self.setLayout(self.dialog_ly)
		self.setWindowTitle((self.datei.replace("_", " ")).replace(".csv",""))


	def createConnects(self):
		self.btn_close.clicked.connect(self.close)

	def processData(self):
		ranks = logFileHandler.read(self.datei)	#Liste
		rev_ranks = sorted(ranks, key = None, reverse = True) 	# Liste umgekehrt sortiert
		formatted_list = []
		for i in range(len(rev_ranks)):
			repl = rev_ranks[i].replace(",", "   ")				# Kommas entfernen
			formatted_list.append(repl)
		ranks_string = "".join(formatted_list)					# Liste zu Strings

		# TODO Spalten abgrenzen/Tabs formatieren
		self.setText(ranks_string)


	def setText(self, ranks):
		self.textarea.setText(ranks)
		self.setFixedSize(350, 300)
