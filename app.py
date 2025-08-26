from flask import Flask, render_template, request
import requests
app = Flask(__name__)

@app.route('/')
def index():
    return render_template("home.html")


@app.route('/catfacts', methods=['GET', 'POST'])
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