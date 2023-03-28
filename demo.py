from pyvpd.rectification import *


image = io.imread("io/input/2.jpg")

vps_3d = []
vps_2d = []

edgelets1 = compute_edgelets(image)
vis_edgelets(image, edgelets1) # Visualize the edgelets

vp1 = ransac_vanishing_point(edgelets1, num_ransac_iter=2000, threshold_inlier=5)
vps_3d.append(vp1)
vp1 = reestimate_model(vp1, edgelets1, threshold_reestimate=5)
vps_2d.append(vp1)
vis_model(image, vp1) # Visualize the vanishing point model

edgelets2 = remove_inliers(vp1, edgelets1, 10)

vp2 = ransac_vanishing_point(edgelets2, num_ransac_iter=2000, threshold_inlier=5)
vps_3d.append(vp2)
vp2 = reestimate_model(vp2, edgelets2, threshold_reestimate=5)
vps_2d.append(vp2)
vis_model(image, vp2) # Visualize the vanishing point model

print(vps_3d)
print(vps_2d)
