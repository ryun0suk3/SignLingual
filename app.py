from flask import Flask,render_template,request, redirect, url_for, flash,jsonify
from flask_mysqldb import MySQL
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://username:password@localhost/db_name'  # Replace with your MySQL database URI
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)


app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'mydb'
app.config['MYSQL_PORT'] = 3308

@app.route("/")
def home():
  return render_template("index.html")

@app.route("/login",methods=['GET', 'POST'])
def login():
  if request.method == 'POST':
        email = request.form['loginEmail']
        password = request.form['loginPassword']
        # Check if the user exists in the database
        user = User.query.filter_by(email=email, password=password).first()
        if user:
            return 'Login successful'
        else:
            return 'Invalid email or password'
  return render_template('login.html')
  

# @app.route("/about")
# def login():
#   return render_template("about.html")

# @app.route("/contact")
# def login():
#   return render_template("contact.html")


if __name__ == "__main__":
  app.run(host='0.0.0.0', debug=True)
