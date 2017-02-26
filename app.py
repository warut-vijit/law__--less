from flask import Flask, request, render_template, url_for, redirect, jsonify
from os import listdir,getcwd
from os.path import isfile, join
import json
from pdf2txt import *
from unigrams import calculate_unigrams
from topic_analysis import *

app = Flask(__name__)

# initialize extensions
print listdir('static/scripts/extensions')
extensions = [f for f in listdir(join('static', 'scripts', 'extensions')) if not isfile(join('static', 'scripts', 'extensions', f))]

def get_extensions():
    html_inject = ""
    for extension in extensions:
        if "config.json" in listdir(join('static', 'scripts', 'extensions', extension)):
            config_text = open(join('static', 'scripts', 'extensions', extension, 'config.json')).read()
            config_json = json.loads(config_text)
            script = open(join('static', 'scripts', 'extensions', extension, extension+".js")).read()
            html_inject += "<script>"+script+"</script>\n"
            html_inject += "<a onclick='"+str(config_json["function"])+"()'>"+str(config_json["name"])+"</a>\n"
    return html_inject

# endpoints
@app.route('/')
def home():
    return render_template("index.html")

@app.route('/upload-target',methods=['POST'])
def upload_target():
    if request.method == "POST" :
        file_key = request.files.keys()[0]
        file_text = request.files[file_key] # of type FileStorage
        cleaned_string = cleaner( pdf2text(file_text) ) # convert pdf to txt
<<<<<<< HEAD
        keywords = get_top_n_words(file_text , 5)
        strings = calculate_unigrams(cleaned_string, keywords) # calculate most important sentences, possibly calculate_unigrams(cleaned_string, keywords)
=======
        strings = calculate_unigrams(cleaned_string) # calculate most important sentences
>>>>>>> master
        out_file = open("output.txt", "w")
        for string in strings:
            out_file.write(string+".")
        out_file.close() # persistent abstract
        return "success"

@app.route('/get-target',methods=['GET'])
def get_target():
    summary = ""
    in_file = open("output.txt", "r")
    for line in in_file.readlines():
        summary += line
    in_file.close()
    os.remove("output.txt")
    return summary

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
    app.run(host='0.0.0.0', port=80, debug=True)
