import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial import distance
from .rectification import * 


class VPDetector:
    def __init__(self, num_ransac_iter=2000, threshold_inlier=10, threshold_reestimate=5):
        self.num_ransac_iter = num_ransac_iter
        self.threshold_inlier = threshold_inlier
        self.threshold_reestimate = threshold_reestimate

    def detect(self, image):
        vps_3d = []
        vps_2d = []

        edgelets1 = compute_edgelets(image)
        vp1_3d = ransac_vanishing_point(edgelets1, num_ransac_iter=self.num_ransac_iter, threshold_inlier=self.threshold_inlier)
        vp1_2d = reestimate_model(vp1_3d, edgelets1, threshold_reestimate=self.threshold_inlier)
        vps_3d.append(vp1_3d)
        vps_2d.append(vp1_2d)

        edgelets2 = remove_inliers(vp1_2d, edgelets1, 10)
        vp2_3d = ransac_vanishing_point(edgelets2, num_ransac_iter=2000, threshold_inlier=self.threshold_inlier)
        vp2_2d = reestimate_model(vp2_3d, edgelets2, threshold_reestimate=self.threshold_inlier)
        vps_3d.append(vp2_3d)
        vps_2d.append(vp2_2d)

        for i in range(len(vps_3d)):
            vps_3d[i] = vps_3d[i] / np.linalg.norm(vps_3d[i])

        self.vps_3d = np.array(vps_3d)
        self.vps_2d = np.array(vps_2d)
        
        # self.vps_3d, self.vps_2d = VPDetector.rearrange_order(image, self.vps_3d, self.vps_2d)
        return self.vps_3d, self.vps_2d

    def showPoints(self, image, save=False, path="vps_2d.png"):
        plt.imshow(image)
        colors = ['red', 'green', 'blue']
        for i, vp_2d in enumerate(self.vps_2d):
            plt.scatter(vp_2d[0], vp_2d[1], c=colors[i])
        plt.show()
        if save:
            plt.savefig(path, dpi=300)

    def showLines(self, image):
        # Visualize the vanishing point model
        vis_model(image, self.vps_2d[0])
        vis_model(image, self.vps_2d[1])

    @staticmethod
    def rearrange_order(image, vps_3d, vps_2d):
        # x and z are horizontal axes
        # y is vertical axis
        vps_2d = vps_2d[:3, :]
        vps_3d = vps_3d[:3, :]
        vps_2d_y = vps_2d[:, 1][..., np.newaxis]
        dist = distance.cdist(vps_2d_y, vps_2d_y, 'euclidean')
        np.fill_diagonal(dist, np.nan)
        horizontal_indexes = np.unravel_index(np.nanargmin(dist), dist.shape)
        for i in range(3):
            if i not in horizontal_indexes:
                y_index = i

        h, w = image.shape[:2]
        image_center = np.array([w // 2, h // 2])

        max = 0
        for i in horizontal_indexes:
            dist = distance.euclidean(vps_2d[i], image_center)
            if dist > max:
                max = dist
                x_index = i

        for i in range(3):
            if i not in [x_index, y_index]:
                z_index = i

        vps_3d = vps_3d[[x_index, y_index, z_index], :]
        vps_2d = vps_2d[[x_index, y_index, z_index], :]
        return vps_3d, vps_2d
