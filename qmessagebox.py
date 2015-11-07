#!/usr/bin/python3
# -*- coding: utf-8 -*-

__author__ = 'cp'

"""
Modul zur Erzeugung der Standard-Messagedialoge (About, Information, Question, ...)
Alle in Klasse QtWidgets.QMessageBox. ...
"""

from PyQt5 import QtWidgets



def about(self):
    QtWidgets.QMessageBox.about(self,
                                u'Über dieses Programm',
                                u'Dieses Programm verwendet den in c\'t 18/2015 vorgestellten Code\
                                 zur sicheren Erstellung und Wiederherstellung von Passwörtern: <a href="http://www.ct.de/yvec">Link</a>')


def warning(self, text):
    QtWidgets.QMessageBox.information(self, u"Warnung",
                                      text,
                                      )
def save_or_not(self):
    status = QtWidgets.QMessageBox.question(self,
                                    u'Ungespeicherte Änderungen',
                                    u'Änderungen in der Domainliste speichern?',
                                    QtWidgets.QMessageBox.Yes, QtWidgets.QMessageBox.No)

    if status == QtWidgets.QMessageBox.Yes:
        return True


def instructions(self):
    QtWidgets.QMessageBox.information(self,
                                      u"Kurze Anleitung",
                                      u'So funktioniert es:\
                                      \n\n1. Sie brauchen auf jeden Fall ein Master-Passwort (MPW).\
                                      Das ist das eine, das man sich merken muss. Deswegen kann \
                                      es auch etwas komplizierter sein.\
                                      \n\n2. Mit diesem MPW und einer sog. Domain wird das Passwort\
                                      für diese Domain erzeugt; also z. B. das Passwort für den \
                                      sowieso-Webshop oder das Onlinebanking.\
                                      \n\n3. Sie können definieren, mit welchen Zeichen (a, A, 1, &, ...)\
                                      das Passwort erzeugt wird, und wie lange es sein soll (5 - 25 Zeichen).\
                                      Den Punkt \"Iterationen\" lässt man am besten bei 4096.\
                                      \n\nACHTUNG: Das selbe Passwort aus der Kombination von MPW und Domain \
                                      kommt nur dann wieder hervor, wenn die Einstellungen die SELBEN sind.\
                                      Es empfiehlt sich daher, die oft gebrauchten Kombis zu speichern und\
                                      für die Liste der Domain-Namen beim Aufruf des Programms zu laden.')


