from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello():
    return "Hello from CI/CD Pipeline! With Jenkins that is triggerd by POLL SCM!"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)