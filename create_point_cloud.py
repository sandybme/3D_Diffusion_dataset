import open3d as o3d
import json 
import cv2
import math
import numpy as np
import matplotlib.pyplot as plt
from ply_util import *
from plotting  import plot_point_cloud
from point_cloud import *

point_cloud = o3d.io.read_point_cloud('/Users/Sandhanakrishnan/Desktop/input/corgi.ply')
points = np.asarray(point_cloud.points)
colors = np.asarray(point_cloud.colors)
channels = {"R":colors[:,0],"G":colors[:,1],"B":colors[:,2]}

pc  = PointCloud(coords=points,channels=channels)
pc = pc.farthest_point_sample(4096)
plot_point_cloud(pc, grid_size=1)
plt.show()