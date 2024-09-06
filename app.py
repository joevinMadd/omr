from flask import Flask

app = Flask("OMR")

@app.route('/', methods = ['GET'])
def home():
    return "Hello, Monka!"

if __name__ == "__main__":
    app.run()
