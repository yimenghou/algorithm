#! /usr/bin/env python
from sklearn import linear_model

clf = linear_model.LinearRegression()
filename = "./laser_calibration_data.txt"

with open(filename) as f:
	content_raw = f.readlines()
	data_lst = [x.strip().split(" ") for x in content_raw] 

X = [[float(i[0])] for i in data_lst]
y = [float(i[1]) for i in data_lst]
clf.fit(X,y)

print "coefficients: ", clf.coef_, clf.intercept_
results = [clf.coef_*i+clf.intercept_ for i in range(6)]
print results