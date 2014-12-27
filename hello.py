# coding=utf8

from ImageResizer.Resize import *

from flask import Flask, send_file
from flask import request
import requests
from PIL import Image
from StringIO import StringIO


app = Flask(__name__)

@app.route("/<int:width>/<int:height>/<mode>")
def hello(width=100, height=100, mode=IMAGE_RESIZE_RULE_CROP_MIDDLE):

    url = request.args.get('url')

    # http://docs.python-requests.org/en/latest/user/quickstart/#errors-and-exceptions
    # try:
    r = requests.get(url)
    # except ConnectionError:
    #     pass

    im = Image.open(StringIO(r.content))

    resized_image = resize_and_crop(im, (width, height), mode)

    return serve_pil_image(resized_image)


def serve_pil_image(pil_img):
    img_io = StringIO()
    pil_img.save(img_io, 'JPEG', quality=70)
    img_io.seek(0)
    return send_file(img_io, mimetype='image/jpeg')


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description='Development Server Help')
    parser.add_argument("-d", "--debug", action="store_true", dest="debug_mode",
                        help="run in debug mode (for use with PyCharm)", default=False)

    cmd_args = parser.parse_args()
    app_options = {}

    if cmd_args.debug_mode:
        app_options["debug"] = True
        app_options["use_debugger"] = False
        app_options["use_reloader"] = False

    app.run(**app_options)