#! -*- coding: utf-8 -*-
# Lab 3, Grubian Eugen

import numpy as np
import pandas as pd
import random as rd
from timeit import timeit
from StringIO import StringIO
import gc

gc.enable()

def numpy_array_init():
	f = open('household_power_consumption.txt','r')
	s = f.read()
	s = s.replace(':',';')
	s = s.replace('/',';')
	s = StringIO(s)
	f.close()
	a = np.genfromtxt(s, delimiter=';', dtype=[('day','i1'),('month','i1'),('year','i2'),('hour','i1'),\
		('minute','i1'),('secunde','i1'),('GAP','f8'),('GRP','f8'),('voltage','f8'),('global_intensity','f8'),\
		('sub_1','f8'),('sub_2','f8'),('sub_3','f8')], skip_header=1, missing_values='?')
	return a[~np.isnan(a['GAP'])]

def pandas_dataframe_init():
	df = pd.read_csv('household_power_consumption.txt', index_col = False, sep = '/|:|;', na_values=['?', ''],\
		names=['day','month','year','hour','minute','secunde','GAP','GRP','voltage','global_intensity','sub_1',\
		'sub_2','sub_3'], skiprows = 1)
	df.dropna()
	return df

def numpy_test():
	numpy_array = numpy_array_init()
	def task1():
		return numpy_array[numpy_array['GAP'] > 5]
	def task2():
		return numpy_array[numpy_array['voltage'] > 235]
	def task3():
		return numpy_array[(numpy_array['global_intensity'] >= 19) & (numpy_array['global_intensity'] <= 20) & \
		(numpy_array['sub_2'] > numpy_array['sub_3'])]
	def task4():
		SAMPLE_SIZE = 500000
		sample = rd.sample(np.arange(numpy_array['day'].size), SAMPLE_SIZE)
		return [np.sum(numpy_array[sample]['sub_1'])/SAMPLE_SIZE, np.sum(numpy_array[sample]['sub_2'])/SAMPLE_SIZE,\
			np.sum(numpy_array[sample]['sub_3'])/SAMPLE_SIZE]
	def task5():
		t5_1 = numpy_array[(numpy_array['hour'] >= 18) & (numpy_array['GAP'] + numpy_array['GRP'] < 6) & \
			(numpy_array['sub_2'] > numpy_array['sub_1']) & (numpy_array['sub_2'] > numpy_array['sub_3'])][::3]
		t5_2 = numpy_array[~((numpy_array['hour'] >= 18) & (numpy_array['GAP'] + numpy_array['GRP'] < 6) & \
			(numpy_array['sub_2'] > numpy_array['sub_1']) & (numpy_array['sub_2'] > numpy_array['sub_3']))][::4]
		return (t5_1, t5_2)
	print "Numpy array tests:"
	print "Test for task1: {0:.2f}s".format(timeit(task1, number=10)/10)
	print "Test for task2: {0:.2f}s".format(timeit(task2, number=10)/10)
	print "Test for task3: {0:.2f}s".format(timeit(task3, number=10)/10)
	print "Test for task4: {0:.2f}s".format(timeit(task4, number=10)/10)
	print "Test for task5: {0:.2f}s".format(timeit(task5, number=10)/10)
	gc.collect()

def pandas_test():
	df = pandas_dataframe_init()
	def task1():
		return df[df['GAP'] > 5]
	def task2():
		return df[df['voltage'] > 235]
	def task3():
		return df[(df['global_intensity'] >= 19) & (df['global_intensity'] <= 20) & (df['sub_2'] > df['sub_3'])]
	def task4():
		SAMPLE_SIZE = 500000
		sample = rd.sample(np.arange(len(df)), SAMPLE_SIZE)
		return [np.sum(df['sub_1'].iloc[sample])/SAMPLE_SIZE, np.sum(df['sub_2'].iloc[sample])/SAMPLE_SIZE, \
			np.sum(df['sub_3'].iloc[sample])/SAMPLE_SIZE]

	def task5():
		t5_1 = df[(df['hour'] >= 18) & (df['GAP'] + df['GRP'] < 6) & (df['sub_2'] > df['sub_1']) & \
			(df['sub_2'] > df['sub_3'])].iloc[::3]
		t5_2 = df[~((df['hour'] >= 18) & (df['GAP'] + df['GRP'] < 6) & (df['sub_2'] > df['sub_1']) & \
			(df['sub_2'] > df['sub_3']))].iloc[::4]
		gc.collect()
		return (t5_1, t5_2)
	print "Pandas dataframe tests:"
	print "Test for task1: {0:.2f}s".format(timeit(task1, number=10)/10)
	print "Test for task2: {0:.2f}s".format(timeit(task2, number=10)/10)
	print "Test for task3: {0:.2f}s".format(timeit(task3, number=10)/10)
	print "Test for task4: {0:.2f}s".format(timeit(task4, number=10)/10)
	gc.collect()
	print "Test for task5: {0:.2f}s".format(timeit(task5, number=10)/10)

def main():
	numpy_test()
	print '---'
	pandas_test()

if __name__ == '__main__':
    main()
