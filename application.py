# coding=utf8
from urlparse import urlparse
import sys

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

application = Flask(__name__)
application.debug = os.environ.get('FLASK_DEBUG') is not None

image_sizes = sizes_from_file('sizes.json')

AWS_HEADERS = {
    'Cache-Control': 'max-age=31556926,public',
    'Content-Type': 'image/jpeg'
}

AWS_ACL = 'public-read'

AWS_BUCKET_NAME = os.environ.get('AWS_BUCKET_NAME')

@application.before_request
def log_request():
    if application.config.get('DEBUG'):
        application.logger.debug(request.json)

@application.route("/view/<int:width>/<int:height>/<mode>")
def view(width=100, height=100, mode=IMAGE_RESIZE_RULE_CROP_NONE):

    im = fetch_image_from_url(request.args.get('url'))
    resized_image = resize_and_crop(im, (width, height), mode)

    img_io = StringIO()
    resized_image.save(img_io, 'JPEG', quality=70)
    img_io.seek(0)
    return send_file(img_io, mimetype='image/jpeg')


@application.route("/", methods=['GET'])
def resize_at_url():

    url_string = request.args.get('url')
    if url_string is not None:

        im = fetch_image_from_url(url_string)

        connection = boto.connect_s3()
        bucket = connection.get_bucket(AWS_BUCKET_NAME)
        application.logger.info("Connecting to bucket %s", AWS_BUCKET_NAME)

        url = urlparse(url_string)
        filename = url[2].split('/')[-1]
        resize_and_save_image(bucket, im, image_sizes, filename)
    else:
        application.logger.info('Received / GET request')

    return "OK"


@application.route("/", methods=['POST'])
def resize_from_post():

    connection = boto.connect_s3()

    application.logger.info('Connecting to s3')
    if request.json is not None:
        records = json.loads(request.json["Message"])["Records"]
        application.logger.info('Decoded %d Records', len(records))

        for record in records:
            process_record(connection, record)
    else:
        # TODO: Use correct HTTP error response
        return "No JSON Found"

    return "OK"


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

        application.logger.debug('Resizing Image (w %d, h %d, m %s) %s', size.width, size.height, size.mode, image_name)

        img_io = StringIO()
        resized_image.save(img_io, 'JPEG', quality=70)

        k = Key(bucket)
        k.key = size.key_name_for_size(image_name)

        application.logger.debug('Creating key name for Image %s', k.key)

        k.set_contents_from_string(img_io.getvalue(), headers=AWS_HEADERS, replace=True, policy=AWS_ACL)


def process_record(connection, record):
    if record['eventName'] == u"ObjectCreated:Put":

        src_bucket = connection.get_bucket(record['s3']['bucket']['name'])
        src_key = Key(src_bucket)
        src_key.key = record['s3']['object']['key']

        img_io = StringIO()
        src_key.get_contents_to_file(img_io)
        img_io.seek(0)
        im = Image.open(img_io)

        dest_bucket = connection.get_bucket(AWS_BUCKET_NAME)
        filename = src_key.key.split('/')[-1]
        resize_and_save_image(dest_bucket, im, image_sizes, filename)


if __name__ == "__main__":
    application.run(host='0.0.0.0')