import flask
import json
import os
import imp
import sys

from flask.templating import render_template


app = flask.Flask(__name__)



@app.route("/predict/<user>/",methods=["GET"])
def predict(user):


    if flask.request.method == "GET":
      try:
        arguments =  flask.request.args
        # print(arguments)

        # filename without extension
        if(arguments.get("pfn")==None):
          pred_filename="prediction"
        else:
          pred_filename = arguments.get("pred_filename")
        

        if(arguments.get("pfl")==None):
          pred_filelocation="uploads"
        else:
          pred_filelocation= arguments.get("pred_filelocation")
        
        print(os.path.join("/mnt/c",user,pred_filelocation,pred_filename+".py"))

        env_path = os.path.join("/mnt/c",user,"uploads/env/lib/python3.9/site-packages")
        sys.path.append(env_path)

        return_string = json.dumps(imp.load_source(pred_filename,os.path.join("/mnt/c",user,pred_filelocation,pred_filename+".py")).predict(arguments))

        sys.path.remove(env_path)

        return return_string

      except Exception as e:
        print(e)
        sys.path.remove(env_path)
        return "Invalid query or prediction file"
    else:
      return "Method Not Allowed"


@app.errorhandler(404)

def not_found(e):
  return render_template("404.html")


if __name__ == '__main__':
   app.run(host='0.0.0.0',port=8080)