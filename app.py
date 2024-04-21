from flask import Flask, render_template, jsonify, request
# from camera import VideoCamera


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
        user = user.query.filter_by(email=email, password=password).first()
        if user:
            return 'Login successful'
        else:
            return 'Invalid email or password'
  return render_template('login.html')
  

@app.route("/register")
def register():
  return render_template("register.html")

@app.route("/about")
def about():
  return render_template("about.html")

@app.route("/contact")
def contact():
  return render_template("contact.html")

@app.route("/speech-to-sign",methods=['GET','POST'])
def speechtosign():
  if request.method == 'POST':
    tests = request.form['letter']
    lis = []
    for word in tests.split():
      alphabet_list = list(word)
      lis.append(alphabet_list)
    return render_template("speechtosign.html", test=lis)
  else:
    return render_template("speechtosign.html", test=[])





# def gen(camera):
#   while True:
#     frame = camera.get_frame()
#     yield (b'--frame\r\n'
#            b'Content-Type: image/jpeg\r\n\r\n' + frame
#            + b'\r\n\r\n')

# @app.route('/video_feed')
# def video_feed():
#   return Response(gen(VideoCamera()),
#                   mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == "__main__":
  app.run(host='0.0.0.0', port='4999', debug=True)
