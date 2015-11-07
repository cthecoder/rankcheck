#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'cp'

import pandas as pd
from ggplot import *

rank = pd.read_csv("Mauersegler_Hardcover.csv")
rank = rank.sort('amount',ascending=False)[:10]
