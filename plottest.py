#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'cp'


# def test():
# 	plt.plot([1,2,3,4,5,6,7], 'ro')
# 	plt.ylabel('some numbers')
# 	plt.show()


# a bar plot with errorbars
import numpy as np
import matplotlib.pyplot as plt

N = 24
motions = [0, 5, 0, 35, 27, 20, 33, 30, 31, 27,20, 32, 30, 34, 27,20, 15, 30, 20, 27, 5, 7, 8 ,9]
#menStd = (2, 3, 4, 1, 2)

ind = np.arange(N)  # the x locations for the groups
width = 0.35  # the width of the bars

fig, ax = plt.subplots()
rects1 = ax.bar(ind, motions, width, color = 'r')

#rects2 = ax.bar(ind + width, womenMeans, width, color = 'y', yerr = womenStd)

# add some text for labels, title and axes ticks
ax.set_ylabel('Motion')
#ax.set_title('Scores by group and gender')
ax.set_xticks(ind + width)
ax.set_xticklabels(('00', '01', '02', '03', '04', '05', '06','07'))

#ax.legend((rects1[0], ('Men')))


def autolabel(rects):
	# attach some text labels
	for rect in rects:
		height = rect.get_height()
		ax.text(rect.get_x() + rect.get_width() / 2., 1.02 * height, '%d' % int(height),
		        ha = 'center', va = 'bottom')


autolabel(rects1)

plt.show()

#if __name__ == "__main__":
#	test()