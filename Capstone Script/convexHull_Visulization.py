#refence: https://gist.github.com/nicoguaro/1cc7474bc2331e48fb64
#modify by: Jinlong Lin

import numpy as np
from scipy.spatial import ConvexHull
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
import sys

# draw annotation face
anno_points = np.loadtxt(sys.argv[1])   # 30 random points in 2-D

hull = ConvexHull(anno_points)

plt.plot(anno_points[:,0], anno_points[:,1], 'x')
cent = np.mean(anno_points, 0)
pts = []
for pt in anno_points[hull.simplices]:
    pts.append(pt[0].tolist())
    pts.append(pt[1].tolist())

pts.sort(key=lambda p: np.arctan2(p[1] - cent[1],
                                p[0] - cent[0]))
pts = pts[0::2]  # Deleting duplicates
pts.insert(len(pts), pts[0])
k = 1.1
color = 'green'
poly = Polygon(k*(np.array(pts)- cent) + cent,
               facecolor=color, alpha=0.2)
poly.set_capstyle('round')
plt.gca().add_patch(poly)

# draw detection face
det_points = np.loadtxt(sys.argv[2])
hull = ConvexHull(det_points)
plt.plot(det_points[:,0], det_points[:,1], 'o')
cent = np.mean(det_points, 0)
pts = []
for pt in det_points[hull.simplices]:
    pts.append(pt[0].tolist())
    pts.append(pt[1].tolist())

pts.sort(key=lambda p: np.arctan2(p[1] - cent[1],
                                p[0] - cent[0]))
pts = pts[0::2]  # Deleting duplicates
pts.insert(len(pts), pts[0])
k = 1.1
color = 'red'
poly = Polygon(k*(np.array(pts)- cent) + cent,
               facecolor=color, alpha=0.2)
poly.set_capstyle('round')
plt.gca().add_patch(poly)


plt.savefig('convex2.png')