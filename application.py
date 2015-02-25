# coding=utf8
from urlparse import urlparse
from flask import Flask, send_file, abort, request
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
application.debug_log_format = '[%(asctime)s] %(levelname)s in %(module)s: %(message)s'

image_sizes = sizes_from_file('sizes.json')

AWS_HEADERS = {
    'Cache-Control': 'max-age=31556926,public',
    'Content-Type': 'image/jpeg'
}

AWS_ACL = 'public-read'

AWS_BUCKET_NAME = os.environ.get('AWS_BUCKET_NAME')

@application.route("/test/<int:width>/<int:height>/<mode>/<name>")
def testRoute(width=100, height=100, mode=IMAGE_RESIZE_RULE_CROP_NONE, name='test/testImage.jpg'):

    im = Image.open('test/testImage.jpg')
    resized_image = resize_and_crop(im, (width, height), mode)

    img_io = StringIO()
    resized_image.save(img_io, 'JPEG', quality=40)
    img_io.seek(0)
    return send_file(img_io, mimetype='image/jpeg')


@application.route("/", methods=['GET'])
def resize_at_url():

    url_string = request.args.get('url')
    if url_string is not None:

        try:
            r = requests.get(url_string)
        except ConnectionError:
            abort(500)

        im = Image.open(StringIO(r.content))

        connection = boto.connect_s3()
        bucket = connection.get_bucket(AWS_BUCKET_NAME)
        application.logger.info("Connecting to bucket %s", AWS_BUCKET_NAME)

        url = urlparse(url_string)
        filename = url[2].split('/')[-1]
        resize_and_save_image(bucket, im, image_sizes, filename)

    return ""


@application.route("/", methods=['POST'])
def resize_from_post():

    connection = boto.connect_s3()

    if request.json is None:
        abort(400)

    records = json.loads(request.json["Message"])["Records"]
    application.logger.info('Decoded %d records', len(records))

    for record in records:
        process_record(connection, record)

    return ""


def process_record(connection, record):
    if record['eventName'] == u"ObjectCreated:Put":
        application.logger.info('Processing Event [%s] for s3://%s/%s', record['eventName'],
                                record['s3']['bucket']['name'],
                                record['s3']['object']['key'])

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


def resize_and_save_image(bucket, image, sizes, image_name):

    for size in sizes:

        resized_key_name = size.key_name_for_size(image_name)

        if bucket.get_key(resized_key_name) is not None:
            application.logger.info('Image %s already exists in bucket, skipping.', resized_key_name)
            continue

        resized_image = resize_and_crop(image, (size.width, size.height), size.mode)
        application.logger.info('Resizing %s to %s', image_name, resized_key_name)

        img_io = StringIO()
        resized_image.save(img_io, 'JPEG', quality=90)

        k = Key(bucket)
        k.key = resized_key_name
        k.set_contents_from_string(img_io.getvalue(), headers=AWS_HEADERS, replace=False, policy=AWS_ACL)

if __name__ == "__main__":
    application.run(host='0.0.0.0', use_reloader=False)