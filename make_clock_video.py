"""Make a set of PNG images of clock and construct video."""
from PIL import Image, ImageDraw, ImageFont
from datetime import timedelta
import glob
import optparse
import os
import os.path
import subprocess


def make_images(frame_rate, duration, width, height):
    """Make a set of images."""
    for filename in glob.glob("tmp/frame*.png"):
        os.remove(filename)
    t_font = ImageFont.truetype("DroidSansMono.ttf", 50)
    f_font = ImageFont.truetype("DroidSansMono.ttf", 32)
    num_frames = int(duration * frame_rate) + 1
    for n in range(0, num_frames):
        t_msec = int(n / frame_rate * 1000 + 0.5)
        t_sec = t_msec // 1000
        t_str = ("%02d:%02d:%02d.%03d" %
                 (t_sec // 3600, (t_sec // 60) % 60,
                  t_sec % 60, (t_msec - t_sec * 1000)))
        f_str = ("frame %5d @ %dfps" % (n, frame_rate))
        image_filename = ("tmp/frame%05d.png" % (n))
        print("%s  %d  %s" % (image_filename, n, t_str))
        image = Image.new("RGBA", (width, height), (255, 255, 255))
        ImageDraw.Draw(image).text((10, 0), t_str, (0, 0, 0), font=t_font)
        ImageDraw.Draw(image).text((10, 55), f_str, (0, 0, 0), font=f_font)
        image.save(image_filename, "PNG")


p = optparse.OptionParser()
p.add_option('--frame-rate', '-f', type='float', action='store',
             help='frame rate in frames per second')
p.add_option('--duration', '-d', type='float', action='store',
             help='duration of video in second')
p.add_option('--width', type='int', default='400',
             help='image width (clock will be top left)')
p.add_option('--height', type='int', default='110',
             help='image height (clock will be top right)')
p.add_option('--just-frames', '-j', action='store_true',
             help='just generate frames and then stop')
p.add_option('--outfile', action='store', default='clock.mp4',
             help='video output file')
(opts, args) = p.parse_args()
if (not opts.frame_rate or not opts.duration):
    p.error("Must specify frame rate and duration (see -h)")

make_images(opts.frame_rate, opts.duration, opts.width, opts.height)
if (opts.just_frames):
    p.error("Frames generated, stopping")
if (os.path.exists(opts.outfile)):
    os.remove(opts.outfile)
subprocess.run(['ffmpeg',
                '-r', str(opts.frame_rate),
                '-i', 'tmp/frame%05d.png',
                '-vcodec', 'libx264',
                '-crf', '25',
                '-pix_fmt', 'yuv420p',
                opts.outfile])
