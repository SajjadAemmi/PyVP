import cv2
from pyvpd import VPDetector


image = cv2.imread("io/input/1.jpg")
image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

vp_detector = VPDetector()
vps_3d, vps_2d = vp_detector.detect(image)
print("vps_3d:", vps_3d)
print("vps_2d:", vps_2d)

vp_detector.showPoints(image, save=True)
vp_detector.showLines(image, save=True)
