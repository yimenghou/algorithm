# -*- coding: UTF-8 -*-

import rosbag, os, copy, time, rospy
from modules.control.proto import *

basepath = "/apollo/py_proto"
exception_lst = ["gnss_pnt_result_pb2"]

for root,dirs,files in os.walk(basepath, topdown=False):
    for name in dirs:
        current_p = os.path.join(root, name)
        if current_p[-5:] == "proto":
            print current_p
            all_f=os.listdir(current_p)
            all_module=[i[:-3] for i in all_f if i[-3:] == ".py"]
            sentence = "__all__=["
            for sub_module in all_module:
            	if sub_module!="__init__" and sub_module not in exception_lst:
            		sentence+= "\""+str(sub_module)+"\""+","
            sentence = sentence[:-1]+"]"
            with open(os.path.join(current_p, '__init__.py'), 'w') as f:
            	f.write(sentence)