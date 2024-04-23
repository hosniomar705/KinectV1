import numpy as np
import cv2

from sensor_msgs.msg import PointCloud2

def Kinect_DepthNormalization_vectorized(depthImage):
    nan_pixels = np.isnan(depthImage)
    neighborhood_size = 5  # Adjust the neighborhood size as needed

    # Create an array of indices for zero pixels
    zero_indices = np.argwhere(nan_pixels)

    for zero_index in zero_indices:
        x, y = zero_index
        x1, x2 = max(x - neighborhood_size // 2, 0), min(x + neighborhood_size // 2 + 1, depthImage.shape[0])
        y1, y2 = max(y - neighborhood_size // 2, 0), min(y + neighborhood_size // 2 + 1, depthImage.shape[1])
        neighborhood_values = depthImage[x1:x2, y1:y2]
        non_zero_values = neighborhood_values[ np.isfinite(neighborhood_values)]

        if non_zero_values.size > 0:
            median_value = np.median(non_zero_values)
            depthImage[x, y] = median_value
            
    return depthImage

def slope(p1,p2):
    if(p1[0] == p2[0]):
        return "error"
    else:
        s = (p2[1]-p1[1])/(p2[0]-p1[0])
        return s
    

def calculate_h_w_d(depth,points):
    
    hi = Kinect_DepthNormalization_vectorized(depth)
    res_r = (2*hi*np.tan(58.35/2))/1280
    res_c = (2*hi*np.tan(45.65/2))/900   
    
    z_values = (hi * 5000).astype(np.uint16)


    # Save the depth image as a 16-bit uint16 image
    cv2.imwrite("depth_image.png", z_values)
    
    
    w = 0 
    h = 0
    d = 0
    
    s = slope(points[0],points[1])
    for i in range(points[0,0],points[1,0]+1):
        y  = round(s*(i - points[0,0]) + points[0,1])
        w += res_r[y,i] 
    
    s = slope(points[0],points[3])
    for i in range(points[0,1],points[3,1]+1):
        if s == "error":
            x  = points[0,0]
        else:
            x  = round((1/s)*(i - points[0,1]) + points[0,0])
            
        
        h += res_c[i,x] 
        
    x = abs((points[0,0]-points[1,0])//2)
    y = abs((points[0,1]-points[3,1])//2)
    center = [x,y]
    d = depth[center[1],center[0]]
          
    return h,w,d
        
