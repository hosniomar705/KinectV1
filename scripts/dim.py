#!/usr/bin/env python
import rospy
import ros_numpy
import cv2
import numpy as np
from sensor_msgs.msg import PointCloud2

def callback(ros_point_cloud):
    point_cloud_array = ros_numpy.numpify(ros_point_cloud)
    z_values = point_cloud_array['z'].copy()
    
    # Scale the depth values to the range [0, 65535] (16-bit)
    z_values = (z_values * 5000).astype(np.uint16)
    rospy.loginfo(z_values.shape)


    # Save the depth image as a 16-bit uint16 image
    cv2.imwrite("depth_image.png", z_values)

    rospy.loginfo("Depth image saved.")
    

def sup():
    rospy.init_node("depthhh", anonymous=True)
    rospy.Subscriber("/camera/depth_registered/points", PointCloud2, callback, queue_size=1, buff_size=52428800)
    rospy.spin()

if __name__ == "__main__":
    sup()
