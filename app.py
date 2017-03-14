from flask import Flask, request, render_template, url_for, redirect, jsonify
from os import listdir,getcwd
from os.path import isfile, join
import md5
import json

from input_cleaning.pdf2txt import *
from summarizer.unigrams import calculate_unigrams
from summarizer.topic_analysis import *
from summarizer.textrank import *
from summarizer.graph_builder import *
from summarizer.tokenizer import *
from sqlalchemy.sql.expression import func
from models import db, Extension

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

'''
Queries for weighting (will move to database)
'''
queries = {}

'''
Endpoints for user interface delivery and document processing
'''

def init_extensions():
    html_inject = ""
    for extension in extensions:
        if "config.json" in listdir(join('static', 'scripts', 'extensions', extension)):
            config_text = open(join('static', 'scripts', 'extensions', extension, 'config.json')).read()
            config_json = json.loads(config_text)
            script = open(join('static', 'scripts', 'extensions', extension, extension+".js")).read()
            html_inject += "<script>"+script+"</script>\n"
            html_inject += "<input type='button' onclick='"+str(config_json["function"])+"()' class='btn btn-extend' value='"+str(config_json["name"])+"'></br>\n"
    return html_inject

# endpoints
@app.route('/')
def home():
    return render_template("index.html")

@app.route('/upload-target',methods=['POST'])
def upload_target():
    if request.method == "POST" :
        # query text entered in search box, if any
        addr_hash = md5.new(request.headers["User-Agent"]).hexdigest()
        query_text = queries[addr_hash] if addr_hash in queries else ""
        
        file_key = request.files.keys()[0]
        file_text = request.files[file_key] # of type FileStorage
        cleaned_string = cleaner( pdf2text(file_text) ) # convert pdf to txt
        sentences = tokenize_text(cleaned_string)
        print sentences
        adj_matrix = create_sentence_adj_matrix(sentences)
        strings = run_textrank_and_return_n_sentences(adj_matrix, sentences, .85, 5)
        out_file = open(md5.new(request.headers["User-Agent"]).hexdigest()+".txt", "w")
        for string in strings:
            out_file.write(string+".")
        out_file.close() # persistent abstract
        return "success"

@app.route('/get-target',methods=['GET'])
def get_target():
    summary = ""
    try:
        in_file = open(md5.new(request.headers["User-Agent"]).hexdigest()+".txt", "r")
        for line in in_file.readlines():
            summary += line
        in_file.close()
        os.remove(md5.new(request.headers["User-Agent"]).hexdigest()+".txt")
        return summary
    except IOError:
        return ""

@app.route('/cases',methods=['GET', 'POST']) # post method for handling queries
def cases():
    if request.method == 'POST':
        query = request.form["query"]
        queries[md5.new(request.headers["User-Agent"]).hexdigest()] = query
        response = render_template("cases.html", extensions=init_extensions(), popup="none")
    else:
        response = render_template("cases.html", extensions=init_extensions(), popup="none")
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate" # HTTP 1.1.
    response.headers["Pragma"] = "no-cache" # HTTP 1.0.
    response.headers["Expires"] = "0" # Proxies.
    return response

@app.route('/features',methods=['GET'])
def features():
    response = render_template("features.html")
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate" # HTTP 1.1.
    response.headers["Pragma"] = "no-cache" # HTTP 1.0.
    response.headers["Expires"] = "0" # Proxies.
    return response

@app.route('/contribute',methods=['GET'])
def contribute():
    response = render_template("contribute.html")
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate" # HTTP 1.1.
    response.headers["Pragma"] = "no-cache" # HTTP 1.0.
    response.headers["Expires"] = "0" # Proxies.
    return response

@app.route('/aboutus',methods=['GET'])
def aboutus():
    response = render_template("aboutus.html")
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate" # HTTP 1.1.
    response.headers["Pragma"] = "no-cache" # HTTP 1.0.
    response.headers["Expires"] = "0" # Proxies.
    return response

'''
Endpoints for distributing extensions
'''

@app.route('/market',methods=['GET'])
def market():
    response = render_template("market.html")
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate" # HTTP 1.1.
    response.headers["Pragma"] = "no-cache" # HTTP 1.0.
    response.headers["Expires"] = "0" # Proxies.
    return response

@app.route('/market/getextensions/',methods=['GET'])
def getextensions():
    offset = int(request.args.get('offset')) if 'offset' in request.args and request.args.get('offset').isdigit() else 0
    maxsize = int(request.args.get('maxsize')) if 'maxsize' in request.args and request.args.get('maxsize').isdigit() else 10
    return jsonify([ext.get_dict() for ext in Extension.query.offset(offset).limit(maxsize).all()])

'''
Interact with database
'''

@app.route('/market/countextensions/',methods=['GET'])
def countextensions():
    return str(Extension.query.count())

@app.route('/market/vote',methods=['GET'])
def vote():
    if 'id' in request.args and 'rating_points' in request.args and 'total_ratings' in request.args:
        rating = request.args.get('rating_points')
        total  = request.args.get('total_ratings')
        Extension.query.get( request.args.get('id') ).rating_points = rating
        Extension.query.get( request.args.get('id') ).total_ratings = total
        db.session.commit()
        return "success"

'''
Initialize database with local extensions
'''
db.app = app
db.init_app(app)
db.create_all(app=app)
#db.create_all(app=app)
extensions = [f for f in listdir(join('static', 'scripts', 'extensions')) if not isfile(join('static', 'scripts', 'extensions', f))]
for extension in extensions:
    if "config.json" in listdir(join('static', 'scripts', 'extensions', extension)):
        config_text = open(join('static', 'scripts', 'extensions', extension, 'config.json')).read()
        config_json = json.loads(config_text)
        ext_object = Extension(
            name=extension,
            author=config_json["author"],
            description=config_json["description"],
            field=config_json["field"],
            rating_points = 0,
            total_ratings = 0
        )
        db.session.add(ext_object)
        db.session.commit() 

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, threaded=True) #debug=True can be added for debugging
