# login.py
from flask import Blueprint, render_template, request, redirect, url_for, session

login_bp = Blueprint('login', __name__)

# Dummy user store
users = {'admin': 'secret'}

@login_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users and users[username] == password:
            session['user'] = username
            return redirect(url_for('home'))
        return "Invalid credentials", 401
    return render_template('login.html')

@login_bp.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login.login'))
