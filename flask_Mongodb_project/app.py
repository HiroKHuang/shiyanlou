from datetime import datetime
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from pymongo import MongoClient

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:woaimiaomiao@localhost/shiyanlou'
app.config['TEMPLATES_AUTO_RELOAD'] = True
db = SQLAlchemy(app)
client = MongoClient('127.0.0.1', 27017)
mongodb = client.shiyanlou

class Article(db.Model):
    __tablename__ = 'articles'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), unique=True)
    created_time = db.Column(db.DateTime)
    category_id = db.Column(db.Integer,db.ForeignKey('categories.id'))
    content = db.Column(db.Text)
    category = db.relationship('Category', backref='article', uselist=False )
    def __init__(self, title, created_time, category, content):
        self.title = title
        self.created_time = created_time
        self.category = category
        self.content = content

    def add_tag(self, tag_name):
        if mongodb.tags.find_one({"ar_id": self.id, "tags": tag_name}):
            print("same tag")
        else:
            mongodb.tags.insert_one({"ar_id": self.id, "tags": tag_name})

    def remove_tag(self, tag_name):
        mongodb.tags.remove({"ar_id": self.id, "tags": tag_name})

    def tags(self):
        for a_id in self.ar_id:
            mongodb.tags.find({"ar_id": a_id})

class Category(db.Model):
    __tablename__= 'categories'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)

    def __init__(self, name):
        self.name = name

def insert_datas():
    java = Category('java')
    python = Category('Python')
    file1 = Article('Hello Java', datetime.utcnow(), java, 'File Content - Java is cool!')
    file2 = Article('Hello Python', datetime.utcnow(), python, 'File Content - Python is cool!')
    db.session.add(java)
    db.session.add(python)
    db.session.add(file1)
    db.session.add(file2)
    db.session.commit()

    file1.add_tag('tech')
    file1.add_tag('java')
    file1.add_tag('linux')
    file2.add_tag('tech')
    file2.add_tag('python')

db.create_all()

@app.route('/')
def index():
    return render_template('index.html', files = Article.query.all())

@app.route('/files/<int:file_id>')
def file_index(file_id):
    return render_template('file.html', contents = Article.query.get_or_404(file_id), tags = mongodb.tags.find({"ar_id": file_id}, {"ar_id": 0,"_id":0}))

@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'),404
