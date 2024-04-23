#!/usr/bin/env python
import calculate_dim
from test.srv import get_dim_srv
from test.srv import get_dim_srvRequest
from test.srv import get_dim_srvResponse

import rospy    
import ros_numpy
import numpy as np
from sensor_msgs.msg import PointCloud2

def handle_get_dim(req):
    point_cloud_array = ros_numpy.numpify(req.frame)
    z_values = point_cloud_array['z'].copy()
    points =np.array(req.points.data, dtype=np.int64).reshape(4, 2)
    h,w,d = calculate_dim.calculate_h_w_d(z_values,points)
    print("HEIGH = " , h)
    print("WIDTH = " , w)
    print("depth = " , d)
    return get_dim_srvResponse(h,w,d)

def get_dim_server():
    rospy.init_node('get_dim_server')
    s = rospy.Service('get_dim', get_dim_srv, handle_get_dim)
    print("Ready to get dimensions.")
    rospy.spin()

if __name__ == "__main__":
    get_dim_server()