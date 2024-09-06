from flask import Flask,render_template

app = Flask("OMR")

@app.route('/', methods = ['GET'])
def home():
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)
