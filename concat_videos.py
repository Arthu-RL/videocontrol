import cv2
import numpy as np
import argparse
import os
import sys
import logging

logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.DEBUG)

parser = argparse.ArgumentParser()
parser.add_argument('--videof-path', dest="videof_path", type=str, required=True)
parser.add_argument('--videos-path', dest="videos_path", type=str, required=True)
parser.add_argument('--margin_width', type=int, default=40)
parser.add_argument('--outdir', type=str, default='./outputs')

args = parser.parse_args()

videof_path = args.videof_path
if not (os.path.exists(videof_path)):
    logging.error("File doesn't exist")
    sys.exit(1)

videos_path = args.videos_path
if not (os.path.exists(videos_path)):
    logging.error("File doesn't exist")
    sys.exit(1)

os.makedirs(args.outdir, exist_ok=True)


videof = cv2.VideoCapture(videof_path)
videos = cv2.VideoCapture(videos_path)

frame_width = int(videof.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(videof.get(cv2.CAP_PROP_FRAME_HEIGHT))
frame_rate = int(videof.get(cv2.CAP_PROP_FPS))
output_width = frame_width * 2 + args.margin_width

logging.info(f"Resolution: {frame_width} x {frame_height} - Output Width: {output_width}")
logging.info(f"FPS: {frame_rate}")


filenamef = os.path.basename(videof_path)
filenames = os.path.basename(videos_path)
extension: str = "."+os.path.splitext(filenamef)[1]

combined_filename = filenamef.replace(extension, "_X_"+filenames)
output_filename = combined_filename.replace(extension, "_video_combined"+extension)
output_path = os.path.join(args.outdir, output_filename)

out = cv2.VideoWriter(filename=output_path, fourcc=cv2.VideoWriter_fourcc(*"mp4v"), fps=frame_rate, frameSize=(output_width, frame_height))


while True:
    retf, framef = videof.read()
    retv, framev = videos.read()

    if not retf or not retv:
        break

    split_region = np.ones((frame_height, args.margin_width, 3), dtype=np.uint8) * 255
    combined_frame = cv2.hconcat([framef, split_region, framev])

    out.write(combined_frame)

videof.release()
videos.release()
out.release()

logging.info(f"Video saved at: {output_path}")
