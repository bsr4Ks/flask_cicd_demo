from flask import Flask, render_template, request, redirect, url_for
from dotenv import load_dotenv
from login import login_bp
import requests
import os


app = Flask(__name__)
load_dotenv()
app.secret_key = os.getenv("FLASK_SECRET_KEY")
app.register_blueprint(login_bp)


def session(user):
    if not user:
        return redirect(url_for("login"))

@app.route('/')
def index():
    session(session.get('user'))
    return render_template("home.html", user=user)


@app.route('/catfacts', methods=['GET', 'POST'])
def catfacts():
    session(session.get('user'))
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
def dogimages():
    session(session.get('user'))
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