from flask import Flask
app = Flask(__name__)

@app.route('/<name>')
def greet(name):
    return "Hello, " + name + "!"

@app.route('/')
def home():
    return "Enter your name in the URL"

if __name__ == '__main__':
    app.run(debug=True)
