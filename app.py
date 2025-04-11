from flask import Flask, request, jsonify,render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'

db = SQLAlchemy(app)

class User(db.Model):
    username = db.Column(db.String(80), primary_key=True)
    password = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    first_name = db.Column(db.String(80), nullable=False)
    last_name = db.Column(db.String(80), nullable=False)
    phone_number = db.Column(db.String(20), nullable=False)
    date_of_registration = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<User {self.username}>'
    
@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter(User.username == username).first()
        if user and user.password == password:
            return redirect(url_for('dashboard', username=user.username))
        elif user and user.password != password:
            return render_template('Login.html', error='Invalid password')
        else:
            return render_template('Login.html', error='User not found')
    return render_template('Login.html')
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['password']
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        phone_number = request.form['phone']
        new_user = User(username=username, password=password, email=email, first_name=first_name, last_name=last_name, phone_number=phone_number)

        try:
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('login'))
        except:
            return render_template('Register.html', error='Username or email already exists')
    return render_template('Register.html')
@app.route('/dashboard/<username>', methods=['GET'])
def dashboard(username):
    return render_template('Dashboard.html', username=username)
@app.route('/logout', methods=['GET'])
def logout():
    return redirect(url_for('login'))

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))  # default to 5000 if PORT not set
    app.run(host='0.0.0.0', port=port)


        