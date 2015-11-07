#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Ruft die Webseite anhand von bookURL und ISBN auf, extrahiert unter Verwendung von Reg EX den Lieferzustand (auf
Lager, soundsoviel vorhanden, Lieferbar in ...) und den Amazon-Verkaufsrang. Falls keine Internetverbindung zustande
kommt: return "None" (für einen neuen Versuch), sonst: return Rank und Lieferstatus
"""

from http.client import HTTPConnection
from re import *
import logging

# import config as c
# import display_data
#  import requests
# checkout https://pypi.python.org/pypi/requests/  und doku: http://docs.python-requests.org/en/latest/

# get = logging.getLogger("data-request")
# get.setLevel(c.LOGGING_LEVEL)

base_url = "www.amazon.de"


class RetrieveData():
	def __init__(self):
		self.returnMessage = ""

	@staticmethod
	def get_rank(book_id):
		# TODO zweites ex für rang in belletristik
		treffer = False
		rex_rank = compile('Nr.\s\d*[.]*\d*')  # "Nr. 9.999, 12.345, 123 ...
		rex_bell_rank = compile('Nr.\s\d*')
		rex_avail_1 = compile('Auf Lager')  # entweder
		rex_avail_2 = compile('Nur noch\s\d+\sauf Lager')  # oder ...
		rex_avail_3 = compile('Lieferbar in')  # Lieferbar in ...
		# TODO put regex in config
		conn = HTTPConnection(base_url)

		try:
			conn.request('GET', "/" + book_id)
			webpage = conn.getresponse()

			if int(
					webpage.status) == 200:  # status OK, 404 = not found etc (https://docs.python.org/3/library/http.client.html
				# get.info("querying web page")
				pagecontent = str(webpage.read())  # content nach abfrage/auswertung löschen? wg speicherbedarf

				if rex_rank.findall(pagecontent)[0]:  # returns Liste von Treffern, [0] ist erster, [1] ist zweiter
					curr_rank = int(str(rex_rank.findall(pagecontent)[0]).lstrip("Nr. ").replace(".", ""))
				else:
					print("kein Rank gefunden")
					curr_rank = 9999999
				try:
					curr_bell_rank = int(str(rex_bell_rank.findall(pagecontent)[1]).lstrip("Nr. "))
					print("currbellrank", curr_bell_rank)
				except:
					print("bellrank nicht ermittelt")

				try:
					curr_available = str(rex_avail_1.findall(pagecontent)[0])
					treffer = True
				except IndexError:
					# get.debug("excluding: less than 20 Ex")
					pass
				try:
					curr_available = str(rex_avail_2.findall(pagecontent)[0]).lstrip("Nur noch ").rstrip(" auf Lager.")
					treffer = True
				except IndexError:
					# get.debug("excluding: exact number avail")
					pass
				try:
					curr_available = str(rex_avail_3.findall(pagecontent)[0])
					treffer = True
				except IndexError:
					# get.debug("excluding: not in stock")
					pass

				if not treffer:  # falls kein Treffer mit den reg-ex: Buch nicht mehr gelistet o.Ã¤.
					curr_available = "unknown"  # Lieferstatus unbekannt (bzw Non-Amazon)

				# get.info("DONE OK")
				conn.close()
				return curr_available, curr_rank, curr_bell_rank  # RÃ¼ckgabe von Lagerstatus und Rang-Nr

			else:
				print(webpage.status)
				# get.error("Keine Verbindung zur Seite")
				returnMessage = "---"
				return returnMessage  # ... sonst: nichts und zurÃ¼ck

		except:
			# get.error("Keine Verbindung zum Internet")
			# display_data.feed_display("", c.CONN_ERR_MSG, "", "", "")
			returnMessage = "---"
			return returnMessage  # ... sonst: nichts

	@staticmethod
	def checkInetConn():
		conn = HTTPConnection("www.google.de")
		fail = False
		try:
			conn.request('GET', "/")
			webpage = conn.getresponse()
			if int(webpage.status) == 200:
				msg = "Verbindung zum Internet ok"
				fail = False
			else:
				msg = "Keine Verbindung zum Internet."
				fail = True

		except:
			msg = "Keine Verbindung zum Internet."
			fail = True

		return msg, fail
