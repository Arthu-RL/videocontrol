import cv2
import math
import argparse
import os
import logging
from tqdm import tqdm

logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.DEBUG)

parser: argparse.ArgumentParser = argparse.ArgumentParser()
parser.add_argument("-v", "--video_path", dest="video_path", help="Caminho do vídeo", type=str, default='')
parser.add_argument("-o", "--outdir", type=str, default='./outputs')
parser.add_argument("-s", "--scale_resolution", dest="scale_resolution", help="Escala para diminuir, ou, aumentar resolução do vídeo", type=float, default=0.5)
parser.add_argument("--fps", dest="fps",  help="FPS dop vídeo de saída", type=float)

args: argparse.Namespace = parser.parse_args()

cap: cv2.VideoCapture = cv2.VideoCapture(args.video_path)

if not cap.isOpened():
    logging.error(f"Error: Unable to open video file {args.video_path}")
    exit(1)

width: int = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height: int = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps: float = float(cap.get(cv2.CAP_PROP_FPS))
total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

logging.info(f"Video capture:")
logging.info(f"width: {width}, height: {height}, fps: {fps}, total_frames: {total_frames}")


resized_width: int = math.ceil(width * args.scale_resolution)
resized_height: int = math.ceil(height * args.scale_resolution)
resized_fps: float = args.fps

logging.info(f"Video output:")
logging.info(f"resized_width: {resized_width}, resized_height: {resized_height}, resized_fps: {resized_fps}")


filename: str = os.path.basename(args.video_path)
filename_extension: str = os.path.splitext(filename)
filename = filename_extension[0]
extension: str = filename_extension[1]
output_path = os.path.join(args.outdir, f"{filename}_down_sized{extension}")

logging.debug("Extra info:")
logging.debug(f"filename: {filename}, extension: {extension}")
logging.debug(f"Output file path: {output_path}")

fourcc: int = cv2.VideoWriter.fourcc(*"mp4v")

writer: cv2.VideoWriter = cv2.VideoWriter(output_path, cv2.CAP_ANY, fourcc, resized_fps, (resized_width, resized_height))

if not writer.isOpened():
    logging.error(f"Error: Unable to open the video writer for output file {output_path}")
    cap.release()
    exit(1)

if not os.path.isdir(args.outdir):
    os.makedirs(os.path.basename(args.outdir), exist_ok=True)


progress_bar = tqdm(total=total_frames, desc="Processing frames", unit="frame")

while True:
    ret, frame = cap.read()

    if not ret:
        break
    
    resized_frame: cv2.Mat = cv2.resize(frame, (resized_width, resized_height))

    writer.write(resized_frame)

    progress_bar.update(1)


cap.release()
writer.release()

progress_bar.close()

logging.info(f"Video saved at: {output_path}")