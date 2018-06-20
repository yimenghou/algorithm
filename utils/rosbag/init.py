import rosbag, os, copy, time, rospy

# basepath = "/apollo/py_proto/"
# for root,dirs,files in os.walk(basepath+"modules", topdown=False):
# 	for name in dirs:
# 		current_p = os.path.join(root, name)
# 		if current_p[-5:] == "proto":
# 			module_name = current_p.replace("/",".")[len(basepath):]
# 			sentence = "from "+module_name+" import *"
# 			print sentence

from modules.third_party_perception.proto import *
from modules.drivers.conti_radar.proto import *
from modules.drivers.canbus.proto import *
from modules.drivers.proto import *
from modules.calibration.republish_msg.proto import *
from modules.localization.proto import *
from modules.map.proto import *
from modules.dreamview.proto import *
from modules.data.proto import *
from modules.control.proto import *
from modules.perception.onboard.proto import *
from modules.perception.obstacle.lidar.segmentation.cnnseg.proto import *
from modules.perception.lib.config_manager.proto import *
from modules.perception.proto import *
from modules.prediction.proto import *
from modules.routing.proto import *
from modules.canbus.proto import *
from modules.planning.proto import *
from modules.monitor.proto import *
from modules.common.adapters.proto import *
from modules.common.monitor_log.proto import *
from modules.common.configs.proto import *
from modules.common.proto import *
