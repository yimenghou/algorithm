#! /usr/bin/env python

import pylab as plt

filename = "./data.txt"

with open(filename) as f:
	content_raw = f.readlines()
	data_lst = [x.strip().split(" ") for x in content_raw] 

X = [[float(i[0])] for i in data_lst]
Y = [float(i[1]) for i in data_lst]

plt.figure()
plt.ion()
plt.axis('equal')

for i in range(len(Y)):		
	plt.plot(X[i], Y[i], "x")
	plt.pause(0.1)
