from flask import Flask, request, render_template, url_for, redirect
app = Flask(__name__)


@app.route('/')
def home():
    return render_template("index.html")

@app.route('/upload-target',methods=['POST'])
def login():
    return str(type(request.files))

@app.route('/cases',methods=['GET'])
def cases():
    return render_template("cases.html")

@app.route('/features',methods=['GET'])
def features():
    return render_template("features.html")

@app.route('/aboutus',methods=['GET'])
def aboutus():
    return render_template("aboutus.html")

if __name__ == '__main__':
    app.run(host='0.0.0.0')
