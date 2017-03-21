# `clock_video`

Generate a video file of a clock.

## Requires

  * `ffmpeg`
  * a bunch of python installs

## Usage

To generate a 60 second video at 25 frames per second:

```
python make_clock_video.py -d 60 -f 25 --outfile clock_60s.mp4
```