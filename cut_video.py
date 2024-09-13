from moviepy.editor import VideoFileClip # clips_array 
from moviepy.video.fx.all import resize
import argparse
import logging
import os
import sys

logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.DEBUG)

parser = argparse.ArgumentParser()
parser.add_argument('--video-path', dest="video_path", type=str)
parser.add_argument('--outdir', type=str, default='./outputs')
parser.add_argument('--start-time', dest="start_time", type=int, default=-1)
parser.add_argument('--end-time', dest="end_time", type=int, default=-1)

args = parser.parse_args()

if args.start_time == -1 or args.end_time == -1:
    logging.warn("Must have start and end time")
    sys.exit(1)

# Load the video file
video = VideoFileClip(args.video_path)

filename = os.path.basename(args.video_path)

logging.info(f"Video to cut: {filename}")
logging.info(f"Dimensions: {video.w}, {video.h}")

# Define the start and end times in seconds
start_time = args.start_time  # Start at 10 seconds
end_time = args.end_time    # End at 20 seconds

new_resolution = (1280, 720)

resized_video = resize(video, newsize=new_resolution)

# Cut the video
cut_video = resized_video.subclip(start_time, end_time)

# Save the new cut video
cut_video.write_videofile(os.path.join(args.outdir, f"subclip_{filename}"), codec="libx264", audio_codec="aac")

# Close the video file to release resources
video.close()

