import argparse
from skimage import io
from pyvpd import VPDetector


parser = argparse.ArgumentParser(description='Vanishing Point Detector')
parser.add_argument("--input", default="io/input/1.jpg", help="input image path", type=str)
parser.add_argument("--output", default="io/output/vps_2d.png", help="output dir path", type=str)
parser.add_argument("--save", default=False, help="whether to save", action="store_true")
args = parser.parse_args()

image = io.imread(args.input)

vp_detector = VPDetector()
vps_3d, vps_2d = vp_detector.detect(image)
print("vps_3d:", vps_3d)
print("vps_2d:", vps_2d)

vp_detector.showPoints(image, save=args.save, path=args.output)
vp_detector.showLines(image)
