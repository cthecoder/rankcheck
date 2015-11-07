#!/usr/bin/python3
# -*- coding: utf-8 -*-
__author__ = 'cp'

"""
Optionen.Dialog
"""

import sys, os

from PyQt5 import QtWidgets, QtCore, Qt
from PyQt5.QtWidgets import *

import qmessagebox
import xmlHandler


class OptionsDialog(QtWidgets.QDialog):

	def __init__(self):
		QtWidgets.QDialog.__init__(self)
		self.autoCheckOn = False
		self.check_intervall = 1
		self.createComponents()
		self.createLayout()
		self.createConnects()

	def createComponents(self):
		self.cb_autoOnOff = QtWidgets.QCheckBox(u"Automatische Abfrage")
		self.cb_autoOnOff.setToolTip(u"Automatische Abfrage in bestimmten Abständen aktivieren")
		self.label_1 = QtWidgets.QLabel(u'im Abstand von: ')
		self.sb_interval = QtWidgets.QSpinBox()
		#self.sb_interval.setPrefix('*')
		self.sb_interval.setSuffix(' Stunden')
		self.sb_interval.setMinimum(1)
		self.sb_interval.setMaximum(24)
		self.sb_interval.setSingleStep(2)
		self.linie1 = QtWidgets.QFrame()
		self.linie1.setMinimumSize(150, 1)
		self.linie1.setFrameShape(QtWidgets.QFrame.HLine)
		self.linie1.setFrameShadow(QtWidgets.QFrame.Sunken)
#		self.linie1.setAlignment(Qt.AlignLeft)

		self.btn_exit = QtWidgets.QPushButton(u"Abbrechen")
		self.btn_save = QtWidgets.QPushButton(u"Übernehmen")



	def createLayout(self):
		self.setWindowTitle(u'Optionen')

		optionsLayout = QtWidgets.QVBoxLayout()
		optionsLayout.addWidget(self.cb_autoOnOff)
		optionsLayout.addWidget(self.label_1)
		optionsLayout.addWidget(self.sb_interval)
		optionsLayout.addWidget(self.linie1)
		buttons_ly = QtWidgets.QHBoxLayout()
		buttons_ly.addWidget(self.btn_save, 0, QtCore.Qt.AlignLeft)
		buttons_ly.addWidget(self.btn_exit, 0, QtCore.Qt.AlignRight)

		optionsLayout.addLayout(buttons_ly)
		self.setLayout(optionsLayout)


	def createConnects(self):

		self.btn_exit.clicked.connect(self.cancelApplication)
		self.btn_save.clicked.connect(self.saveAndExit)

	def checkAutoState(self):
		if self.cb_autoOnOff.isChecked():
			return True
		else:
			return False

	def checkIntervall(self):
		autoCheckIntervall = self.sb_interval.value()
		return autoCheckIntervall

	def cancelApplication(self):
		self.close()

	def saveAndExit(self):
		if self.checkAutoState():
			self.check_intervall = self.checkIntervall()
			self.autoCheckOn = True;
			print('AutoCheck alle ', self.check_intervall, ' Stunden')
		else:
			self.autoCheckOn = False
		self.close()
