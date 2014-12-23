# flask-images

A [flask](http://flask.pocoo.org) application designed to run on Amazon Elastic Beanstalk [Worker Environment Tier](http://docs.aws.amazon.com/elasticbeanstalk/latest/dg/using-features-managing-env-tiers.html) that responds to SQS messages generated from new images uploaded to a specific S3 bucket.

flask-images will resize newly uploaded images into a set of pre-configured sizes and re-upload the images into size specific directories for easy, predictable access.

# Python Environment Setup

Getting your python environment setup on OSX is not too hard. [This guide](http://docs.python-guide.org/en/latest/starting/install/osx/) is a good place to start.

**tldr; install homebrew and do the following:**

```sh
brew install python
pip install virtualenv
```

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


# Bits 

## Image Resizing Examples

https://gist.github.com/sigilioso/2957026

[1]: http://flask.pocoo.org
[2]: http://docs.python-guide.org/en/latest/