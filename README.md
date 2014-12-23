# flask-images

A flask application designed to run on elastic beanstalk as a worker that resizes images stored in S3 and place them back in S3 in a useful place.

# Dependencies

You need python, pip, and virtualenv installed first.

Python comes with OSX, you might need sudo for these two commands - don't worry because the rest of the decencies will be installed locally in the python virtual environment.

```sh
easy_install pip
pip install virtualenv
```

# Running flas-images

Setup your local development.

```sh
git clone git@github.com:jessedc/flask-images.git
cd flask-images
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
```

It's a simple python [flask][1] application. 

```sh
python hello.py
```

Take your browser to [http://localhost:5000](http://localhost:5000)


# Bits 

# Image Resizing Examples

https://gist.github.com/sigilioso/2957026

[1]: http://flask.pocoo.org