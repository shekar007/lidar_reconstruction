#!/usr/bin/env python
import rospy
import math
import random
import numpy as np
import matplotlib.pyplot as plt
from lidar_project.srv import lidar
def custom_trig(angle):
    
    radianme = math.radians(angle)
    
    if angle <= 45:
        theta = math.sin(radianme) * (math.sqrt(2) - 1) + 1
    else:
        theta = math.cos(radianme) * (1 - math.sqrt(2)) + math.sqrt(2)
    
    return theta

def lidar_client(centerX, centerY):
    rospy.wait_for_service('scan')
    try:
        lidar_scan = rospy.ServiceProxy('scan', lidar)
        response = lidar_scan(centerX, centerY)
        return response.lidar_array
    except rospy.ServiceException as e:
        print("Service call failed:", str(e))

if __name__ == "__main__":
    
    rospy.init_node('lidar_client')
    count=1
    map_size = 400
    map_image = np.ones((map_size, map_size), dtype=np.uint8) * 255

    centerX = 200
    centerY = 200
    total =0
    lidar_data = lidar_client(centerX, centerY)
    if(lidar_data!=None):
        resolution = 1 
        for i in range(0, len(lidar_data), 2):
            angle = lidar_data[i]
            distance = lidar_data[i+1]

            x = int(distance * np.cos(np.radians(angle))) + centerX
            y = int(distance * np.sin(np.radians(angle))) + centerY
            if 0 <= x < map_size and 0 <= y < map_size:
                # Calculate the bounds for the dot
                dot_size = 2
                xmin = max(0, x - dot_size)
                xmax = min(map_size - 1, x + dot_size)
                ymin = max(0, y - dot_size)
                ymax = min(map_size - 1, y + dot_size)
                map_image[ymin:ymax, xmin:xmax] = 0 
    angle1 = 0
    while(angle1 < 360):
        theta = lidar_data[angle*2]
        r = lidar_data[2*angle +1]
        d = angle %90
        rmax = int(custom_trig(d)*r)
        rmid = (r + rmax)/2
        x = int(rmid * np.cos(np.radians(angle1))) + centerX
        y = int(rmid * np.sin(np.radians(angle1))) + centerY
        ldata = lidar_client(x, y)
        if(ldata!=None):
            resolution = 100 
            for i in range(0, len(ldata), 2):
                angle = ldata[i]
                distance = ldata[i+1]

                a= int(distance * np.cos(np.radians(angle))) + x
                b = int(distance * np.sin(np.radians(angle))) + y
                if 0 <= a < map_size and 0 <= b < map_size:
                    dot_size = 2
                    xmin = max(0, a - dot_size)
                    xmax = min(map_size - 1, a + dot_size)
                    ymin = max(0, b - dot_size)
                    ymax = min(map_size - 1, b+ dot_size)

                    map_image[ymin:ymax, xmin:xmax] = 0
        angle1+=35
        
    

    plt.imsave('map.jpg', map_image, cmap='gray')

    plt.imshow(map_image, cmap='gray')
    plt.show()

