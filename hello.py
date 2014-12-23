from flask import Flask
from flask import request
import requests

app = Flask(__name__)

@app.route("/")
def hello():

    url = request.args.get('url')

    img_request = requests.get(url)

    return "Hello World!"

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