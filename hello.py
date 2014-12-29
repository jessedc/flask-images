# coding=utf8
import os

from ImageResizer.Resize import *

from flask import Flask, send_file
from flask import request
import requests
from PIL import Image
from StringIO import StringIO
import json
from requests.packages.urllib3.connection import ConnectionError

app = Flask(__name__)

json_data = open('image_sizes.json')
image_sizes = json.load(json_data)["sizes"]
json_data.close()


@app.route("/view/<int:width>/<int:height>/<mode>")
def view(width=100, height=100, mode=IMAGE_RESIZE_RULE_CROP_NONE):

    url = request.args.get('url')

    # http://docs.python-requests.org/en/latest/user/quickstart/#errors-and-exceptions
    # try:
    r = requests.get(url)
    # except ConnectionError:
    #     pass

    im = Image.open(StringIO(r.content))

    resized_image = resize_and_crop(im, (width, height), mode)

    return serve_pil_image(resized_image)

@app.route("/<int:width>/<int:height>/<mode>")
def resize_all(width, height, mode):

    url = request.args.get('url')

    # http://docs.python-requests.org/en/latest/user/quickstart/#errors-and-exceptions
    try:
        r = requests.get(url)
    except ConnectionError:
        return "Request Exception"

    im = Image.open(StringIO(r.content))

    resize_and_save_image(im, image_sizes)

    return "OK"


def serve_pil_image(pil_img):
    img_io = StringIO()
    pil_img.save(img_io, 'JPEG', quality=70)
    img_io.seek(0)
    return send_file(img_io, mimetype='image/jpeg')


def resize_and_save_image(image, sizes):

    for size in sizes:
        resized_image = resize_and_crop(image, (size["width"], size["height"]), size["mode"])
        filename = "output/{0}/{1}/{2}/{3}".format(size["width"], size["height"], size["mode"], "testfile.jpg")

        # TODO: replace this with S3 code
        if not os.path.exists(os.path.dirname(filename)):
            os.makedirs(os.path.dirname(filename))

        resized_image.save(filename, 'JPEG', quality=70)


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