# coding=utf8
from urlparse import urlparse

from flask import Flask, send_file
from flask import request

import os
import requests
import boto
from boto.s3.key import Key
from PIL import Image
from StringIO import StringIO
from requests.packages.urllib3.connection import ConnectionError

from ImageResizer.Resize import *
from ImageResizer.Size import *


app = Flask(__name__)

image_sizes = sizes_from_file('sizes.json')

AWS_HEADERS = {
    'Cache-Control': 'max-age=31556926,public',
    'Content-Type': 'image/jpeg'
}

AWS_ACL = 'public-read'

AWS_BUCKET_NAME = os.environ.get('AWS_BUCKET_NAME')

@app.route("/view/<int:width>/<int:height>/<mode>")
def view(width=100, height=100, mode=IMAGE_RESIZE_RULE_CROP_NONE):

    im = fetch_image_from_url(request.args.get('url'))
    resized_image = resize_and_crop(im, (width, height), mode)

    img_io = StringIO()
    resized_image.save(img_io, 'JPEG', quality=70)
    img_io.seek(0)
    return send_file(img_io, mimetype='image/jpeg')


@app.route("/", methods=['GET'])
def resize_at_url():

    url_string = request.args.get('url')

    im = fetch_image_from_url(url_string)

    connection = boto.connect_s3()
    bucket = connection.get_bucket(AWS_BUCKET_NAME)

    url = urlparse(url_string)
    filename = url[2].split('/')[-1]
    resize_and_save_image(bucket, im, image_sizes, filename)

    return "OK"

@app.route("/", methods=['POST'])
def resize_from_post():

    # url_string = request.args.get('url')
    #
    # im = fetch_image_from_url(url_string)
    #
    # connection = boto.connect_s3()
    # bucket = connection.get_bucket(AWS_BUCKET_NAME)
    #
    # url = urlparse(url_string)
    # filename = url[2].split('/')[-1]
    # resize_and_save_image(bucket, im, image_sizes, filename)

    return "OK-POST"


def fetch_image_from_url(url):
    # http://docs.python-requests.org/en/latest/user/quickstart/#errors-and-exceptions
    try:
        r = requests.get(url)
    except ConnectionError:
        return None

    return Image.open(StringIO(r.content))


def resize_and_save_image(bucket, image, sizes, image_name):

    for size in sizes:
        resized_image = resize_and_crop(image, (size.width, size.height), size.mode)

        img_io = StringIO()
        resized_image.save(img_io, 'JPEG', quality=70)

        k = Key(bucket)
        k.key = size.key_name_for_size(image_name)
        k.set_contents_from_string(img_io.getvalue(), headers=AWS_HEADERS, replace=True, policy=AWS_ACL)


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