"""Make a set of PNG images of clock and construct video."""
from PIL import Image, ImageDraw, ImageFont
from datetime import timedelta
import optparse
import os
import os.path
import subprocess


def make_images(frame_rate, duration, tmp="tmp"):
    """Make a set of images."""
    subprocess.run("rm tmp/frame????.png", shell=True)
    font = ImageFont.truetype("ClearSans-Bold.ttf", 50)
    num_frames = int(duration * frame_rate) + 1
    for n in range(0, num_frames):
        t = n / frame_rate
        tsec = int(t)
        t_str = ("%02d:%02d:%02d.%02d" %
                 (tsec // 3600, (tsec // 60) % 60,
                  tsec % 60, int((t - tsec) * 100)))
        image_filename = ("tmp/frame%05d.png" % (n))
        print("%s  %s" % (image_filename, t_str))
        image = Image.new("RGBA", (310, 74), (255, 255, 255))
        ImageDraw.Draw(image).text((10, 0), t_str, (0, 0, 0), font=font)
        image.save(image_filename, "PNG")


p = optparse.OptionParser()
p.add_option('--frame-rate', '-f', type='float', action='store',
             help='frame rate in frames per second')
p.add_option('--duration', '-d', type='float', action='store',
             help='duration of video in second')
p.add_option('--just-frames', '-j', action='store_true',
             help='just generate frames and then stop')
p.add_option('--outfile', action='store', default='clock.mp4',
             help='video output file')
(opts, args) = p.parse_args()
if (not opts.frame_rate or not opts.duration):
    p.error("Must specify frame rate and duration (see -h)")

make_images(opts.frame_rate, opts.duration)
if (opts.just_frames):
    p.error("Frames generated, stopping")
if (os.path.exists(opts.outfile)):
    os.remove(opts.outfile)
subprocess.run(['ffmpeg',
                '-r', str(opts.frame_rate),
                '-s', '310x74',
                '-i', 'tmp/frame%05d.png',
                '-vcodec', 'libx264',
                '-crf', '25',
                '-pix_fmt', 'yuv420p',
                opts.outfile])
