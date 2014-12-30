# flask-images

[![Build Status](https://travis-ci.org/jessedc/flask-images.svg?branch=master)](https://travis-ci.org/jessedc/flask-images)

A [flask](http://flask.pocoo.org) application designed to run on Amazon Elastic Beanstalk [Worker Environment Tier](http://docs.aws.amazon.com/elasticbeanstalk/latest/dg/using-features-managing-env-tiers.html) that responds to SQS messages generated from new images uploaded to a specific S3 bucket.

flask-images will resize newly uploaded images into a set of pre-configured sizes and re-upload the images into size specific directories for easy, predictable access.

# Python Environment Setup

Getting your python environment setup on OSX is not too hard. [This guide](http://docs.python-guide.org/en/latest/starting/install/osx/) is a good place to start.

**tldr; install homebrew and do the following:**

```sh
brew install python
pip install virtualenv
```

> Future: Create a vagrant environment for this project. (suggested base box [here](https://vagrantcloud.com/notch-interactive/boxes/trusty64-python))

# Running flask-images

```sh
git clone git@github.com:jessedc/flask-images.git
cd flask-images
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
python hello.py
```

Take your browser to [http://localhost:5000](http://localhost:5000)

# Required Environment Variables


 - **AWS_ACCESS_KEY_ID** AWS access key
 - **AWS_SECRET_ACCESS_KEY** AWS secret
 - **AWS_BUCKET_NAME** The name of the bucket the image will be uploaded too


# Size Configuration

The app will automatically resize the input image based on a fixed set of sizes read from a `size.json` file locaded in the root directory.

```json
{ "sizes": [
  {"width":193, "height": 130, "mode": "resize-crop"},
  ...
  ]
}
  
```

# Resizing Modes

The app has two resize modes, `resize` and `resize-crop`. 

Resize will resize the image to within the parameters you specifcy and keep the aspect ratio. 

Resize-crop will do the first resize then crop to the exact size from the centre point.  


# Links

- https://gist.github.com/sigilioso/2957026
- http://sullerton.com/2012/02/debugging-a-flask-app-inside-pycharm/
- https://pillow.readthedocs.org/handbook/tutorial.html#using-the-image-class
- http://docs.aws.amazon.com/elasticbeanstalk/latest/dg/create_deploy_Python_flask.html
- http://docs.python-requests.org/en/latest/user/quickstart/#make-a-request
- http://flask.pocoo.org/docs/0.10/
- https://github.com/mikeboers/Flask-Images


[1]: http://flask.pocoo.org
[2]: http://docs.python-guide.org/en/latest/