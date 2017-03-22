# `clock_video`

Generate a video file of a clock.

## Requires

  * `ffmpeg`
  * `Pillow` fork of the `PIL` Python image library (`pip install Pillow`)

## Usage

To generate a 60 second video at 24 frames per second:

```
python make_clock_video.py -d 60 -f 24 --outfile clock_60s.mp4
```

The font included `DroidSansMono.ttf` is under [Apache 2](http://www.apache.org/licenses/LICENSE-2.0) license.
