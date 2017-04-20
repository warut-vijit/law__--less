from flask import Flask, request, render_template, url_for, redirect, jsonify
from os import listdir,getcwd
from os.path import isfile, join
import os
import md5
import json
import logging
import subprocess as spr
import datetime

from input_cleaning.pdf2txt import *
from summarizer.unigrams import calculate_unigrams
from summarizer.topic_analysis import *
from summarizer.textrank import *
from summarizer.graph_builder import *
from summarizer.tokenizer import *
from summarizer.topic_extractor import *
from untitled import *
from sqlalchemy.sql.expression import func
from models import db, Extension, User, Document
from utils import encryptxor 

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

'''
Queries and active users
'''
queries = {}
users = {}
active_email = []

'''
Endpoints for user interface delivery and document processing
'''

# endpoints
@app.route('/')
@app.route('/home')
def home():
    return render_template("index.html")

@app.route('/upload-target',methods=['POST'])
def upload_target():
    if request.method == "POST" :
        
        #os.chdir("~/Documents/SP17/less_is_more/HackIllinois2017")
        print os.getcwd()
        print "hi \n \n \n \n"

        addr_hash = md5.new(request.headers["User-Agent"]).hexdigest()
        if addr_hash not in users:
            logging.warning("Rejected unauthorized summary request.")
            return ""
        user_name = users[addr_hash]['name']
        user_id = User.query.filter_by(name=user_name).first().id
        query_text = queries[addr_hash] if addr_hash in queries else ""
        
        file_key = request.files.keys()[0]
        file_text = request.files[file_key] # of type FileStorage

        cleaned_string = cleaner( pdf2text(file_text) ) # convert pdf to txt 

        #write stuff to files so we can read in sub processes
        with open("cleaned.txt", "w") as f:
            f.write(cleaned_string)
        with open("query.txt", "w") as f:
            f.write(query_text)
        with open("user.txt", "w") as f:
            f.write(addr_hash)

        spr_analytics = spr.Popen(['python','untitled.py'])
        logging.warning(spr_analytics.communicate())
        adj_matrix = np.array(json.loads(open('cleaned.txt').read()))
        logging.warning("Successfully did some shit")

        sentences = tokenize_text(cleaned_string)
        #print sentences
        #stemmed_sentences = clean_document_and_return_sentances(cleaned_string)
        #adj_matrix = create_sentence_adj_matrix(sentences)
        #adj_matrix = update_graph_with_query(adj_matrix, query_text)
        strings = run_textrank_and_return_n_sentences(adj_matrix, sentences, .85, 5, query = query_text)
        
        doctext = "\n".join(strings)
        doc_obj = Document(
            user_id=user_id,
            text=doctext
        )
        db.session.add(doc_obj)
        db.session.commit()
        logging.warning("Successfully uploaded document for user %s" % user_name)
        return "success"
    else:
        return "wrong method"

@app.route('/get-target',methods=['GET'])
def get_target():
    addr_hash = md5.new(request.headers["User-Agent"]).hexdigest()
    if addr_hash not in users:
        logging.warning("Rejected unauthorized summary request.")
        return ""
    # get user's id as doc backref
    user_name = users[addr_hash]['name']
    user_id = User.query.filter_by(name=user_name).first().id
    doc_obj = Document.query.filter_by(user_id=user_id).order_by(Document.created_at.desc()).first()
    logging.error(Document.query.filter_by(user_id=user_id).count())
    if doc_obj is not None:
        logging.warning("Successfully retrieved summary for user %s" % user_name)
        return encryptxor("imaginecup2017", doc_obj.text)
    logging.warning("Could not located a summary for user %s" % user_name)
    return ""

@app.route('/cases',methods=['GET', 'POST']) # post method for handling queries
def cases():
    if request.method == 'POST' and "query" in request.args:

        addr_hash = md5.new(request.headers["User-Agent"]).hexdigest()
        if addr_hash not in users:
            logging.warning("Rejected unauthorized summary request.")
            return ""
        user_name = users[addr_hash]['name']
        user_id = User.query.filter_by(name=user_name).first().id

        query = request.args.get('query')
        queries[addr_hash] = query
        with open("query.txt", "w") as f:
            f.write(query)
        with open("user.txt", "w") as f:
            f.write(addr_hash)

        spr_analytics = spr.Popen(['python','untitled.py'])
        logging.warning(spr_analytics.communicate())
        adj_matrix = np.array(json.loads(open('cleaned.txt').read()))

        sentences = tokenize_text(cleaned_string)
        #print sentences
        #stemmed_sentences = clean_document_and_return_sentances(cleaned_string)
        #adj_matrix = create_sentence_adj_matrix(sentences)
        #adj_matrix = update_graph_with_query(adj_matrix, query_text)
        strings = run_textrank_and_return_n_sentences(adj_matrix, sentences, .85, 5, query = query_text)

        doctext = "\n".join(strings)
        doc_obj = Document(
            user_id=user_id,
            text=doctext
        )
        db.session.add(doc_obj)
        db.session.commit()
        logging.error(Document.query.filter_by(user_id=user_id).count())
        logging.warning("Successfully placed query for user %s" % user_name)
    response = render_template("cases.html")
    return response

@app.route('/features',methods=['GET'])
def features():
    response = render_template("features.html")
    return response

@app.route('/profile',methods=['GET'])
def profile():
    response = render_template("profile.html")
    return response

@app.route('/aboutus',methods=['GET'])
def aboutus():
    response = render_template("aboutus.html")
    return response

@app.route('/sponsors',methods=['GET'])
def sponsors():
    response = render_template("sponsors.html")
    return response

'''
Endpoints for distributing extensions
'''

@app.route('/market',methods=['GET'])
def market():
    response = render_template("market.html")
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

@app.route('/market/uploadextension',methods=['POST'])
def uploadextension():
    logging.warning(request.files.keys())
    if len(request.files.keys()) < 2:
        logging.warning("User attempted to upload invalid extension")
        return redirect("/market")
    config_json = json.loads(request.files["config"].read())
    ext_object = Extension(
        name= config_json["name"],
        author=config_json["author"],
        description=config_json["description"],
        field=config_json["field"],
        rating_points = 0,
        total_ratings = 0,
        code = request.files["code"].read()
    )
    db.session.add(ext_object)
    db.session.commit()
    logging.warning("Successfully added extension %s" % config_json["name"])
    return redirect("/market")

'''
Login system, interacts with database
'''

@app.route('/login/getcredentials')
def getcredentials():
    addr_hash = md5.new(request.headers["User-Agent"]).hexdigest()
    return jsonify(users[addr_hash]) if addr_hash in users else ""

@app.route('/login/verify')
def verify():
    q = User.query.filter(User.name==request.args.get("username")).first()
    if q is not None and q['password_hash'] == md5.new(request.args.get("password")).hexdigest():
        addr_hash = md5.new(request.headers["User-Agent"]).hexdigest()
        users[addr_hash] = q
        return "success"
    return "fail"

@app.route('/login/signup')
def signup():
    q = User.query.filter(User.username==request.args.get("username")).first()
    if q is not None:
        return "fail"
    user_object = User(
        name=request.args.get("name"),
        username=request.args.get("username"),
        password_hash=md5.new(request.args.get("password")).hexdigest(),
        since=datetime.date.today(),
        ends=datetime.date.today() + datetime.timedelta(days=365)
    )
    addr_hash = md5.new(request.headers["User-Agent"]).hexdigest()
    users[addr_hash] = user_object.get_dict()
    db.session.add(user_object)
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
        try:
            config_text = open(join('static', 'scripts', 'extensions', extension, 'config.json')).read()
            code_text = open(join('static', 'scripts', 'extensions', extension, extension+'.js')).read()
            config_json = json.loads(config_text)
            ext_object = Extension(
                name=config_json["name"],
                author=config_json["author"],
                description=config_json["description"],
                field=config_json["field"],
                rating_points = 0,
                total_ratings = 0,
                code = code_text
            )
            db.session.add(ext_object)
            db.session.commit()
        except IOError:
            logging.error("Failed to upload extension file %s" % extension)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, threaded=True, debug=True) #debug=True can be added for debugging
