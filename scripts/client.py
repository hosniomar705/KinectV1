from test.srv import get_dim_srv
from test.srv import get_dim_srvRequest
from test.srv import get_dim_srvResponse

import numpy as np
import cv2
import ros_numpy
import rospy
from std_msgs.msg import Int64MultiArray
from sensor_msgs.msg import PointCloud2

global dimensions
selected_coordinates=[]

# Define a mouse callback function
def click_event(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        # Capture the pixel coordinates and add them to the list
        selected_coordinates.append([x, y])
  
        
def callback(ros_point_cloud):
    
    selected_coordinates.clear()    
    point_cloud_array = ros_numpy.numpify(ros_point_cloud)
    z_values = point_cloud_array['z'].copy()
    
    # Scale the depth values to the range [0, 65535] (16-bit)
    z_values = (z_values * 5000).astype(np.uint16)
    cv2.imshow("image", z_values)
    # Set the mouse callback function for the window
    cv2.setMouseCallback("image", click_event)
    print(selected_coordinates)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

        
    # Flatten the 2D array into a 1D array
    flattened_array = [item for sublist in selected_coordinates for item in sublist]

    # Create an Int64MultiArray message
    int64_multi_array = Int64MultiArray(data=flattened_array)
    
    resp = dimensions(ros_point_cloud,int64_multi_array)
    print(resp.width)
 

    


def sup():
    rospy.init_node("depthhh", anonymous=True)
    rospy.Subscriber("/camera/depth_registered/points", PointCloud2, callback, queue_size=1, buff_size=52428800)


if __name__ == "__main__":
    rospy.wait_for_service('get_dim')
    print("Requesting")
    try:
        dimensions = rospy.ServiceProxy('get_dim', get_dim_srv)
        sup()
        
    except rospy.ServiceException as e:
        print("Service call failed: %s"%e)
    
    
        
    rospy.spin()
    
# from test.srv import get_dim_srv
# from test.srv import get_dim_srvRequest
# from test.srv import get_dim_srvResponse

# import cv2
# import ros_numpy
# import rospy
# from std_msgs.msg import Int64MultiArray
# from sensor_msgs.msg import PointCloud2

# global dimensions
# selected_coordinates = []

# # Define a mouse callback function
# def click_event(event, x, y, flags, param):
#     if event == cv2.EVENT_LBUTTONDOWN:
#         # Capture the pixel coordinates and add them to the list
#         selected_coordinates.append((x, y))
#         print(f"Selected pixel coordinates: ({x}, {y})")
        
        
# def callback(ros_point_cloud):
   
    
#     point_cloud_array = ros_numpy.numpify(ros_point_cloud)
#     cv2.imshow("imageBEFORE", point_cloud_array['z'])
    
#     # Set the mouse callback function for the window
#     cv2.setMouseCallback("imageafterfilter", click_event)
#     cv2.waitKey(0)
#     cv2.destroyAllWindows()
    
#     # Flatten the 2D array into a 1D array
#     flattened_array = [item for sublist in selected_coordinates for item in sublist]

#     # Create an Int64MultiArray message
#     int64_multi_array = Int64MultiArray(data=flattened_array)
    
#     resp = dimensions(ros_point_cloud,int64_multi_array)
#     print(resp.width)
 

    


# def sup():
#     rospy.init_node("depthhh", anonymous=True)
#     rospy.Subscriber("/camera/depth_registered/points", PointCloud2, callback, queue_size=1, buff_size=52428800)


# if __name__ == "__main__":
#     rospy.wait_for_service('get_dim')
#     print("Requesting")
#     try:
#         dimensions = rospy.ServiceProxy('get_dim', get_dim_srv)
#         sup()
        
#     except rospy.ServiceException as e:
#         print("Service call failed: %s"%e)
    
    
        
#     rospy.spin()
    