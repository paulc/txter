
import os,sys
from functools import wraps
from flask import Flask,abort,flash,g,redirect,request,render_template,session,url_for
from flaskext.wtf import Form,TextField,PasswordField,BooleanField,DateTimeField, \
                         RadioField,SelectField,SelectMultipleField,TextAreaField, \
                         required,length
from proxy import ReverseProxied
from mediaburst import MediaBurst,MediaBurstError

DEBUG = os.environ.get('DEBUG',False)
SECRET_KEY = os.urandom(32)

app = Flask(__name__)
app.config.from_object(__name__)

class LoginForm(Form):
    user = TextField(u"Username",description="Mediaburst Username",validators=[required()])
    password = PasswordField(u"Password",description="Mediaburst Password",validators=[required()])

class TxtForm(Form):
    to = TextField(u"To",validators=[required()])
    content = TextAreaField(u"Content",validators=[required(),length(min=1,max=459)])

@app.route('/',methods=("GET","POST"))
def root():
    if 'user' in session:
        mb = MediaBurst(**session['user'])
        txt_form = TxtForm()
        if txt_form.validate_on_submit():
            response = mb.send(**txt_form.data)
            flash(response)
        return render_template("index.html",txt_form=txt_form,credit=mb.credit())
    else:
        return redirect(url_for("login"))

@app.route('/credit',methods=("GET","POST"))
def credit():
    if 'user' in session:
        mb = MediaBurst(**session['user'])
        return render_template("credit.html",credit=mb.credit())
    else:
        return redirect(url_for("login"))

@app.route('/logout')
def logout():
    session = None
    return redirect(url_for("login"))

@app.route('/login',methods=("GET","POST"))
def login():
    login_form = LoginForm()
    if login_form.validate_on_submit():
        try:
            mb = MediaBurst(**login_form.data)
            mb.credit()
            flash(u"Login Successful","success")
            session['user'] = login_form.data
            session.permament = True
            return redirect(url_for("root"))
        except MediaBurstError,e:
            flash(u"Login Failed: %s" % e.message,"error")
        except urllib2.HTTPError,e:
            flash(u"HTTP Error: %s" % e.msg,"error")
        except urllib2.URLError,e:
            flash(u"Network Error: %s" % e.reason.strerror.capitalize(),"error")
    return render_template("login.html",login_form=login_form)

if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    host = os.environ.get('HOST', '0.0.0.0')
    if os.environ.get('PROXY'):
        app.wsgi_app = ReverseProxied(app.wsgi_app)
    app.run(host=host, port=port)
