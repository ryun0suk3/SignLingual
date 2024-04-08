from flask import Flask, render_template, jsonify

app = Flask(__name__)

@app.route("/")
def home():
  return render_template("index.html")

@app.route("/login")
def login():
  return render_template("login.html")

# @app.route("/about")
# def login():
#   return render_template("about.html")

# @app.route("/contact")
# def login():
#   return render_template("contact.html")


if __name__ == "__main__":
  app.run(host='0.0.0.0', debug=True)
