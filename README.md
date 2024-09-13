# videocontrol

Repo for video manipulation

## Rodar códigos

Concat videos

```bash
python concat_videos.py --videof-path="/path/to/your/video1.mp4" --videos-path="/path/to/your/video2.mp4" --outdir="./outputs"
```

Cut video

```bash
python cut_video.py --video-path="/path/to/your/video.mp4" ---start-time=10 --end-time=50
```

Downsize vídeo, lower FPS, smaller file size

```bash
python downsize.py -v /path/to/your/video.mp4 -o ./output_dir -s 0.5 --fps 30.0
```
