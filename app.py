from flask import Flask, render_template, request, redirect, url_for, session, flash

from flask_sqlalchemy import SQLAlchemy
import subprocess
import os
from face import capture_and_store_face_data

app = Flask(__name__)
app.secret_key = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

# Create database tables before requests
@app.before_request
def before_request():
    db.create_all()
@app.route('/')
def home():
    return render_template('index.html')
@app.route('/home_page',methods=['Post'])
def index():
    return render_template('homepage.html')

@app.route('/add_face', methods=['POST'])
def add_face():
    name = request.form['name']  # Get the name from the form
    capture_and_store_face_data(name)  # Call the function to capture and store facial data

    return render_template('index.html', message='Face data captured successfully!')

# ... (other routes)
@app.route('/recognize_face', methods=['POST'])
def recognize_face():
    message = None
    try:
        subprocess.run(["python", "recognition.py"])
        # message=f'Face Recognition started'

    except Exception as e:
        message=f'Error running recognition: {str(e)}'

    return render_template('index.html', message=message)

# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username, password=password).first()

        if user:
            session['username'] = username
            return redirect(url_for('landing'))
        else:
            flash('Invalid login credentials', 'error')

    return render_template('login.html')

# Registration route
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        existing_user = User.query.filter_by(username=username).first()

        if existing_user:
            flash('Username already exists', 'error')
        else:
            new_user = User(username=username, password=password)
            db.session.add(new_user)
            db.session.commit()
            flash('Registration successful. You can now log in.', 'success')

    return render_template('register.html')

# Logout route
@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))
# Landing page route
@app.route('/landing')
def landing():
    if 'username' in session:
        return render_template('landing.html')
    else:
        return redirect(url_for('login'))

@app.route('/ourteam')
def ourteam():
    if 'username' in session:
        return render_template('ourteam.html')
    else:
        return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)
