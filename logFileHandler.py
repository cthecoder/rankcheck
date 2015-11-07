#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import logging


# import config as c


# fileops = logging.getLogger("file-ops")
# fileops.setLevel(c.LOGGING_LEVEL)


def write(datei, rankdata):
	file = open('data/' + datei, "a")
	file.write(str(rankdata) + "\n")
	file.close()


def read(datei):
	file = open('data/' + datei, "r")
	data = file.readlines()  # ausgabe als string, zeile für zeile
	file.close()
	return data
