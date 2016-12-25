from flask import Flask,render_template,redirect,url_for
from flask import request
from flask_bootstrap import Bootstrap
from flask.ext.wtf import Form
from wtforms.validators import Required
from wtforms import StringField,SubmitField
from flask.ext.sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
from os import path
import os

basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
bootstrap = Bootstrap(app)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///' +os.path.join(basedir,'data.sqlite')
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] =True
db = SQLAlchemy(app)

class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(64),unique=True)
    users =db.relationship('User',backref='role')

    def __repr__(self):
        return '<Role %r>' % self.name

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(64),unique=True,index=True)
    role_id = db.Column(db.Integer,db.ForeignKey('roles.id'))

    def __repr__(self):
        return '<User %r>' % self.username

class NameForm(Form):
    name = StringField('what is your name?',validators=[Required])
    submit = SubmitField('submit')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/user/<name>')
def user(name):
    return render_template('user.html', name=name)

@app.route('/login/',methods=['GET','POST'])
def login():
    name = None
    form = NameForm()

    if form.validate_on_submit():
        name = form.name.data
        form.name.data = ''
    return  render_template('login.html',form=form,name=name)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'),404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'),500

@app.route('/upload',methods=['GET','POST'])
def upload():
    if request.method == 'POST':
        f = request.files['file']
        basepath = path.abspath(path.dirname(__file__))
        upload_path = path.join(basepath,'static/upload/')
        f.save(upload_path+secure_filename(f.filename))
        return redirect(url_for('upload'))
    return render_template('upload.html')

if __name__ == '__main__':
    app.run(debug=True)
