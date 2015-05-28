import subprocess
import logging
from logging.handlers import RotatingFileHandler
from flask import Flask, render_template, request, url_for
from flask.ext.script import Manager
from flask.ext.bootstrap import Bootstrap
from flask.ext.moment import Moment
from flask.ext.wtf import Form
from wtforms import StringField, SubmitField, HiddenField
from wtforms.validators import Required
import threading

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string'

manager = Manager(app)
bootstrap = Bootstrap(app)
moment = Moment(app)

def open_an_ssh(hostname):
    cmd = 'DISPLAY=:03.0 xterm -e "ssh %s"' % hostname 
    p = subprocess.Popen(cmd, stdout = subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE, shell=True)
    out,err = p.communicate()

def sean_thread(hostname):
    threads = []
    t = threading.Thread(target=open_an_ssh, args=(hostname,))
    threads.append(t)
    t.start()

class SwitchForm(Form):
    name = HiddenField('Switch being accessed', validators=[Required()])

@app.route("/leaf1")
def leaf1():
    sean_thread('leaf1') 
    return render_template('index.html')

@app.route("/leaf2")
def leaf2():
    sean_thread('leaf2') 
    return render_template('index.html')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')


if __name__ == '__main__':
    handler = RotatingFileHandler('log.log', maxBytes=10000, backupCount=1)
    handler.setLevel(logging.INFO)
    app.logger.addHandler(handler)    
    manager.run()
