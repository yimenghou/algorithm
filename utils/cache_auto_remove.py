#! /usr/bin/env python
import os,time,getpass,shutil

homedir = os.path.join("/home", getpass.getuser())

#add the removal path here in the list
rm_path = ["/apollo/data/core", \
			"/apollo/data/log", \
			os.path.join(homedir, ".cache/bazel", "_bazel_"+getpass.getuser())]
T = 60

while True:

	for sub_path in rm_path:

		file_lst = os.listdir(sub_path)
		print "Check path: ", sub_path, 
		if not file_lst:
			print ": No files found."
			continue

		for file_item in file_lst:
			file_name = os.path.join(sub_path, file_item)
			[os.unlink(file_name) if not os.path.isdir(file_name) else shutil.rmtree(file_name)]
			print "> removing: ", file_name
	
	time.sleep(T)