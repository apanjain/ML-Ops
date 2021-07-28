import logging
import flask
import json
import os
import imp
import sys

from flask.templating import render_template
from secure_producer import run_producer

app = flask.Flask(__name__)

logging.basicConfig(level=logging.DEBUG)

SHARED_STORAGE_MOUNT_POINT = "/mnt/c"


@app.route("/prediction")
def pred():
    return render_template("predict.html")


@app.route("/training")
def train():
    return render_template("train.html")


@app.route("/predict/<user>/", methods=["GET", "POST"])
def predict(user):

    if flask.request.method == "POST" or flask.request.method == "GET":
        try:
            arguments = flask.request.args
            # print(arguments)

            # filename without extension
            if(arguments.get("pred_filename") == None):
                pred_filename = "prediction"
            else:
                pred_filename = arguments.get("pred_filename")

            if(arguments.get("pred_filelocation") == None):
                pred_filelocation = ""
            else:
                pred_filelocation = arguments.get("pred_filelocation")

            pred_filepath = os.path.join(SHARED_STORAGE_MOUNT_POINT, user, "uploads",
                                         pred_filelocation, pred_filename+".py")

            print(pred_filepath)

            # add to sys path to include user installed packages.
            env_path = os.path.join(
                SHARED_STORAGE_MOUNT_POINT, user, "uploads/env/lib/python3.9/site-packages")
            sys.path.append(env_path)

            return_string = json.dumps(imp.load_source(
                pred_filename, pred_filepath).predict(arguments))

            # remove path as soon as processing is done
            sys.path.remove(env_path)
            return return_string

        except Exception as e:
            print(e)
            sys.path.remove(env_path)
            return str(e)
    else:
        return "Method Not Allowed"


@app.route("/train/<user>/", methods=["GET", "POST"])
def train_msg(user):

    if flask.request.method == "POST" or flask.request.method == "GET":
        try:
            arguments = flask.request.args
            # print(arguments)

            # filename without extension
            if(arguments.get("train_filename") == None):
                train_filename = "train.py"
            else:
                train_filename = arguments.get("train_filename")

            if(arguments.get("train_filelocation") == None):
                train_filelocation = "."
            else:
                train_filelocation = arguments.get("train_filelocation")

            # clear the existing logfile
            logfile_path = os.path.join(
                SHARED_STORAGE_MOUNT_POINT, user, "uploads", train_filelocation, "training.log")
            try:
                with open(logfile_path, 'w') as fp:
                    pass
            except Exception as e:
                print(e)
            # parameters for kafka message
            message = {
                'ml_username': user,
                'train_file_location':
                    train_filelocation,
                'train_file_name': train_filename
            }
            # request sent to kafka
            run_producer(message)
            # log-file is generated for mk1 at some location e.g. mk1/logs.txt
            print("Training request received.")
            return "Request for Model Training submitted."

        except Exception as e:
            print(e)
            return "Invalid username or training file location"
    else:
        return "Method Not Allowed"


@app.route("/logs/<user>/")
def livefeed(user):
    try:
        arguments = flask.request.args
        train_filelocation = "." if arguments.get(
            "train_filelocation") == None else arguments.get("train_filelocation")
        logfile_path = os.path.join(
            SHARED_STORAGE_MOUNT_POINT, user, "uploads", train_filelocation, "training.log")
        with open(logfile_path, 'r') as file:
            string = file.read()

        string = """
        <h2>Training Logs will be printed here!</h2>
        <hr />
        <p>{}</p>""".format(string.replace("\n", "</p><p>"))
        # print(string)
        return string
    except Exception as e:
        return str(e)


@app.errorhandler(404)
def not_found(e):
    return render_template("404.html")


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
