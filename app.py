
import os,sys
from flask import Flask,abort,flash,redirect,request,render_template,session,url_for
from flaskext.wtf import Form,TextField,PasswordField,BooleanField,DateTimeField, \
                         RadioField,SelectField,SelectMultipleField,TextAreaField, \
                         required,length
from proxy import ReverseProxied

DEBUG = os.environ.get('DEBUG',False)
SECRET_KEY = os.urandom(32)

app = Flask(__name__)
app.config.from_object(__name__)

class LoginForm(Form):
    name = TextField(u"Account",description="Account Name",validators=[required(),length(min=2,max=5)])
    password = PasswordField(u"Password",description="A Password",validators=[required()])
    check = BooleanField(u"A Checkbox")
    checkA = BooleanField(u"A")
    checkB = BooleanField(u"B")
    checkC = BooleanField(u"C")
    date = DateTimeField(u"The Date")
    text = TextAreaField(u"Some Text",validators=[length(min=10)])
    options = RadioField(u"Some Options",default="b",choices=[("a","Choice A"),("b","Choice B"),("c","Choice C")])
    select = SelectField(u"Some Options",default="b",choices=[("a","Choice A"),("b","Choice B"),("c","Choice C")])
    select_multiple = SelectMultipleField(u"Some Options",default=["a","b"],choices=[("a","Choice A"),("b","Choice B"),("c","Choice C")])

@app.route('/')
def root():
    flash("Info","info")
    flash("Error","error")
    flash("Success","success")
    flash("None")
    return render_template("index.html")

@app.route('/login',methods=("GET","POST"))
def login():
    login_form = LoginForm()
    if login_form.validate_on_submit():
        flash("Form OK")
        return redirect(url_for("root"))
    return render_template("login.html",login_form=login_form)

if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    host = os.environ.get('HOST', '0.0.0.0')
    if os.environ.get('PROXY'):
        app.wsgi_app = ReverseProxied(app.wsgi_app)
    app.run(host=host, port=port)
