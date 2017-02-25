from flask import Flask, request, render_template, url_for, redirect, jsonify
from os import listdir,getcwd
from os.path import isfile, join
import json

app = Flask(__name__)

# initialize extensions
extensions = [f for f in listdir(join(getcwd(), 'extensions')) if not isfile(join(getcwd(), 'extensions', f))]

def get_extensions():
    html_inject = ""
    for extension in extensions:
        if "config.json" in listdir(join(getcwd(), 'extensions', extension)):
            config_text = open(join(getcwd(), 'extensions', extension, 'config.json')).read()
            config_json = json.loads(config_text)
            html_inject += "<p>"+config_json["name"]+"</p>"
    return html_inject

# endpoints
@app.route('/')
def home():
    return render_template("index.html")

@app.route('/upload-target',methods=['POST'])
def upload_target():
    return str(type(request.files))

@app.route('/diag',methods=['GET'])
def diag():
    return jsonify(extensions)

@app.route('/cases',methods=['GET'])
def cases():
    return render_template("cases.html", extensions=get_extensions())

@app.route('/features',methods=['GET'])
def features():
    return render_template("features.html")

@app.route('/aboutus',methods=['GET'])
def aboutus():
    return render_template("aboutus.html")

if __name__ == '__main__':
    app.run(host='0.0.0.0')
