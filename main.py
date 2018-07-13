#coding=utf-8
from flask import Flask
app = Flask(__name__)
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc
from datetime import datetime
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///.\\foo.db'
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = 1#True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = 1#True
app.secret_key = 'vtheno'
app.config["USERNAME"] = 'vtheno'
app.config["PASSWD"] = 'admin'
db = SQLAlchemy(app)
class Post(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(80))
    body = db.Column(db.Text)
    pub_date = db.Column(db.DateTime)
    pub_date_str = db.Column(db.String(40))
    def __init__(self,title,body,pub_date=None):
        self.title = title
        self.body = body
        self.pub_date = datetime.now() if pub_date is None else pub_date
        self.pub_date_str = str(self.pub_date)[0:-7]
    def __repr__(self):
        return "< Post {} >".format(self.title)

# db.session.add_all( [ db.Model instance ] )
# db.session.commit()
# db.session.delete( xxInstance.query.filter_by(xxx) )

from flask.views import MethodView
from flask import render_template
from flask import abort

from flask import request
from flask import session
from flask import redirect
from flask import url_for
from flask import flash

from vhelp import login_required

def getLines():
    if 'username' not in session:
        return [("Home","/"),
                ("Email","#"),
                ("Login","/login"),]
    else:
        return [("Home","/"),
                ("Email","#"),
                ("Logout","/logout"),
                ('Add Post','/addpost'),]
def getTitles():
    #posts = Post.query.all()
    posts = Post.query.order_by(desc(Post.pub_date))
    #print posts
    return [(post.title,post.pub_date_str) for post in posts]

def getPosts():
    #posts = Post.query.all()
    posts = Post.query.order_by(desc(Post.pub_date))
    return [(post.title,
             post.body,
             post.pub_date_str) for post in posts]
from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import HtmlFormatter

def addPost(title,body):
    lexer = get_lexer_by_name("python", stripall=True)
    formatter = HtmlFormatter(linenos=True,cssstyle='default')
    result = highlight(body, lexer, formatter)
    p = Post( title, result )
    db.session.add(p)
    flag = db.session.commit()
    return flag
class IndexView(MethodView):
    def get(self):
        return render_template('index.html',
                               getLines=getLines,
                               getTitles=getTitles,
                               getPosts=getPosts,)
    def post(self):
        return self.get()
# from werkzeug.security import generate_password_hash,check_password_hash
# global_username = None
class LoginView(MethodView):
    def get(self):
        return render_template('login.html',
                               getLines=getLines,
                               getTitles=getTitles)
    def post(self):
        required = ['username','passwd']
        for r in required:
            if r not in request.form:
                flash('Error: {0} is required.'.format(r) )
                return redirect(url_for('login'))
        username = request.form['username']
        passwd = request.form['passwd']
        if username == app.config["USERNAME"] and passwd == app.config["PASSWD"]:
            session["username"] = global_username
        else:
            flash("Username doesn't exist or incorrect password")
        return redirect(url_for("login"))
class LogoutView(MethodView):
    @login_required
    def get(self):
        if 'username' in session:
            session.pop('username',None)
            flash("Logout success!")
            return redirect(url_for('login'))
        else:
            flash("Your need login!")
            return redirect(url_for('login'))
    @login_required
    def post(self):
        return self.get()
class AddPostView(MethodView):
    @login_required
    def get(self):
        return render_template('addpost.html',
                               getLines=getLines,
                               getTitles=getTitles)
    @login_required
    def post(self):
        title = request.form['title']
        body = request.form['body']
        flag = addPost(title,body)
        flash(" post success! ")
        return redirect(url_for("login"))

methods=["GET","POST"]
app.add_url_rule('/',view_func=IndexView.as_view('index'),methods=methods)
app.add_url_rule('/login',view_func=LoginView.as_view('login'),methods=methods)
app.add_url_rule('/logout',view_func=LogoutView.as_view('logout'),methods=methods)
app.add_url_rule('/addpost',view_func=AddPostView.as_view('addpost'),methods=methods)

from flask_script import Manager
app.debug = 1
manager = Manager(app)
if __name__ == '__main__':
    #app.run(port=80)
    manager.run()
