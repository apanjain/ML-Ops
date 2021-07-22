import flask
import os
import sys
app = flask.Flask(__name__)


@app.route("/predict/<user>/", methods=["GET"])
def predict(user):
    if flask.request.method == "GET":
        arguments = flask.request.args
        # print(user, arguments)
        try:
            dir_path = os.path.join(os.path.dirname(
                __file__), 'shared_storage', str(user))
            print(dir_path)
            sys.path.insert(0, dir_path)
            print(sys.path)
            print(os.listdir(dir_path))
            model = __import__(dir_path,level=0).prediction
            sys.path.remove(dir_path)
            return str(model.predict(arguments))
        except Exception as e:
            print(e)
            return "User or Prediction file does not exist"
    else:
        return "Method Not Allowed"


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
