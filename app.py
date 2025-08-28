from flask import Flask, render_template, request, redirect, url_for, session
from dotenv import load_dotenv
from functools import wraps
import requests
import os

app = Flask(__name__)

FLASK_SECRET_KEY=fbb60b6a4c8b457f061f60098608e8cce718c45b5c2db279
app.secret_key = FLASK_SECRET_KEY

users = {'admin': 'secret'}

# Decorator to enforce login
def require_login(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('user'):
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users and users[username] == password:
            session['user'] = username
            return redirect(url_for('index'))
        return "Invalid credentials", 401
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))

@app.route('/')
@require_login
def index():
    return render_template("home.html", user=session.get('user'))

@app.route('/catfacts', methods=['GET', 'POST'])
@require_login
def catfacts():
    fact = None
    if request.method == "POST":
        try:
            response = requests.get("https://catfact.ninja/fact", verify=False)
            data = response.json()
            fact = data.get("fact")
        except Exception as e:
            print(f"Error fetching cat fact: {e}")
    return render_template("catfacts.html", fact=fact)

@app.route('/dogimages', methods=['POST', 'GET'])
@require_login
def dogimages():
    image_url = None
    if request.method == "POST":
        try:
            response = requests.get("https://dog.ceo/api/breeds/image/random", verify=False)
            data = response.json()
            if data["status"] == "success":
                image_url = data["message"]
        except Exception as e:
            print(f"Error fetching dog image: {e}")
    return render_template("dogimages.html", image_url=image_url)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
