import flask

app = flask.Flask(__name__)

@app.route("/")
def home():
  return "<h1> Bot is online <h1>"

app.run("0.0.0.0")