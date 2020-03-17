from flask import Flask, render_template, url_for, flash, redirect
from forms import RegistrationForm, LoginForm
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import select
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, inspect, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm.session import Session, sessionmaker
import datetime as dt
from sqlalchemy.dialects.postgresql import JSON


app = Flask(__name__)

engine = create_engine('postgresql://postgres:root@localhost/carstock')

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:root@localhost/carstock'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

Base = declarative_base()   
Session = sessionmaker()
metadata = MetaData()

class ErsatzteileAlchemy(db.Model):
    __tablename__ = 'ersatzteile_alchemy'
    Base.metadata.create_all(engine)
    Artikelnummer = db.Column(db.Integer, primary_key=True)
    Bezeichnung = db.Column(db.String(120), unique=False, nullable=False)
    Details = db.Column(db.String(120), unique=False, nullable=True)
    Geraet = db.Column(db.String(120), unique=False, nullable=True)

    def __init__(self, Artikelnummer, Bezeichnung, Details, Geraet):
        self.Artikelnummer = Artikelnummer
        self.Bezeichnung = Bezeichnung
        self.Details = Details
        self.Geraet = Geraet

    def __repr__(self):
        return "Artikelnummer{}, Bezeichnung={}, Details={}, Gerät={}"\
                .format(self.Artikelnummer, self.Bezeichnung, self.Details, self.Geraet)
        #return '<%r>' % self.Bezeichnung
        #return 'self.Artikelnummer'

#db.create_all()
#db.session.commit()
#print(ErsatzteileAlchemy)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    
    def __init__(self, username, email):
        self.username = username
        self.email = email

    def __repr__(self):
        #return '<User %r>' % self.username
        return self
        

app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'admin' or request.form['password'] != 'admin':
            error = 'Invalid Credentials. Please try again.'
        else:
            return redirect(url_for('/index'))
    return render_template('login.html', error=error)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ersatzteilliste')
def ersatzteilliste():
    Ersatzteile = ErsatzteileAlchemy.query.all()
    return render_template('ersatzteilliste.html',Ersatzteile = Ersatzteile)


@app.route('/carstock')
def carstock():
    return render_template('index.html')

@app.route('/bestellungen')
def bestellungen():
    return render_template('bestellungen.html')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)