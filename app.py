from flask import Flask, render_template, request, redirect, url_for, session, Response
from flask_mysqldb import MySQL
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
import cv2
import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing import image

model = tf.keras.models.load_model('signlingual_final_tanvi.h5')
LABELS = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 
          'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', 
          'del', 'space', 'nothing']

def recognize(img):
    img = np.resize(img, (224,224,3))
    img = np.expand_dims(img, axis=0)
    img = np.asarray(img)
    img = img/255.0
    classes = model.predict(img)
    pred_id = np.argmax(classes)  
    return pred_id



global output
output=""
cam = cv2.VideoCapture(0)



def gen():                          #generator
    global img_name, char_op 
    while(True):
        success, frame=cam.read()    
        rec_start=(100,160)
        rec_end=(420,560)
        rec_col=(255,0,0)
        frame=cv2.rectangle(frame,rec_start,rec_end,rec_col,thickness=2)   
        '''
        sucess: 
            boolean value. 
            returns true if python is able to capture video
        frame:
            a numpy array that represents the first image captured by the the VideoCamera
        '''
        crop_sign=frame[rec_start[1]:rec_end[1], rec_start[0]:rec_end[0]]
        # img=cv2.cvtColor(crop_sign, cv2.COLOR_BGR2GRAY)
        # img = cv2.GaussianBlur(img, (5,5), 0)
        pred_img = cv2.resize(crop_sign, (224,224), interpolation=cv2.INTER_AREA)
        y_pred = recognize(pred_img)
        # char_op = chr(y_pred + 65)
        char_op = LABELS[y_pred]
        cv2.rectangle(frame, (80,600), (680,680), (0,0,0), -1)
        cv2.putText(frame, "Predicted Sign: "+char_op, (100,660), cv2.FONT_HERSHEY_SIMPLEX, 2, (255,255,0), 2) 

        if not success:
            print("Capture not Successful")
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  
            # concat frame one by one and show result
            
            #yield lets the execution to continue and generates from until alive

def pr():
    global output
    output+=char_op
    return(output)



app = Flask(__name__)
app.secret_key = 'test'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'user-system'
app.config['MYSQL_PORT'] = 3306

mysql = MySQL(app)

@app.route("/")
def home():
    return render_template("index.html")

@app.route('/login', methods=['GET', 'POST'])
def login():
    message = ''
    if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
        email = request.form['email']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM user WHERE email=%s AND password=%s', (email, password))
        user = cursor.fetchone()
        if user:
            session['loggedin'] = True
            #session['userid'] = user['userid']
            session['name'] = user['name']
            session['email'] = user['email']
            message = 'Logged in successfully'
            return render_template('index.html', message=message)
        else:
            message = 'Please enter correct email/password'
    return render_template('login.html', message=message)



@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('name', None)
    session.pop('email', None)
    return redirect(url_for('login'))

@app.route('/register', methods=['GET','POST'])
def register():
    message = ''
    if request.method == 'POST' and 'name' in request.form and 'email' in request.form and 'password' in request.form:
        username = request.form['name']
        email = request.form['email']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM user WHERE email=%s', (email,))
        account = cursor.fetchone()
        if account:
            message = 'Account Already Exists'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            message = 'Invalid Email'
        elif not username or not password or not email:
            message = 'Please Fill all Details'
        else:
            cursor.execute('INSERT INTO user VALUES(%s,%s,%s)', (username, email, password, ))
            mysql.connection.commit()      
            message = 'Register Successfully!!'
    elif request.method == 'POST':
        message = 'Please Fill all Details'
    return render_template('register.html', message=message) 

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
    else:
        lis = []
    return render_template("speechtosign.html", test=lis)

@app.route('/sign-to-speech')  #landing
def signtospeech():
    return render_template("signtospeech.html")

@app.route('/sign-to-speech/video')
def video():
    return Response(gen(),mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/sign-to-speech/capture')
def capture():
    return render_template("signtospeech.html", output=pr())

@app.route('/sign-to-speech/reset')
def reset():
    global output
    output=""
    return render_template("signtospeech.html", output=output)

@app.route('/sign-to-speech/del_last')
def del_last():
    global output
    output=output[:-1]
    return render_template("signtospeech.html", output=output)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port='4999', debug=True)
