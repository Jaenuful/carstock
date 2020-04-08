from flask import Flask, render_template, url_for, flash, redirect, request, jsonify, make_response
from forms import RegistrationForm, LoginForm
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import select
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, inspect, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm.session import Session, sessionmaker
import datetime as dt
from sqlalchemy.dialects.postgresql import JSON
from flask_wtf import FlaskForm
from wtforms import SelectField
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

app = Flask(__name__)

engine = create_engine('postgresql://postgres:root@localhost/carstock')
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:root@localhost/carstock'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)
#Base = declarative_base()   
#Session = sessionmaker()
#metadata = MetaData()

#    def __init__(self, Artikelnummer, Bezeichnung, Details, Geraet):
#        self.Artikelnummer = Artikelnummer
#        self.Bezeichnung = Bezeichnung
#        self.Details = Details
#        self.Geraet = Geraet

#    def __repr__(self):
 #       return "Artikelnummer{}, Bezeichnung={}, Details={}, Gerät={}"\
  #              .format(self.Artikelnummer, self.Bezeichnung, self.Details, self.Geraet)
        #return '<%r>' % self.Bezeichnung
        #return 'self.Artikelnummer'
#db.create_all()
#db.session.commit()
#print(ErsatzteileAlchemy)

class ErsatzteileAlchemy(db.Model):
    __tablename__ = 'ersatzteile_alchemy'
    Artikelnummer = Column (Integer(), primary_key=True) 
    Bezeichnung = Column (String(), unique=False, nullable=False)
    Details = Column (String(), unique=False, nullable=True)
    Geraet = Column (String(), unique=False, nullable=True)
#    ErsatzteileKonrad = db.relationship('ErsatzteileKonrad')

class ErsatzteileKonrad(db.Model):
    __tablename__ = 'ersatzteile_konrad'
    Anzahl = Column(Integer(), primary_key = True)
    Artikelnummer = Column (Integer(), primary_key=True) 
 #   Bezeichnung = input(f"ErsatzteileAlchemy for '{ersatzteile_alchemy.Bezeichnung}': $")
 #   Artikelnummer = db.realtionship('ErsatzteileAlchemy'), Column (Integer(), ForeignKey) 
    Bezeichnung = Column(Integer(), primary_key=False)
    Ablaufdatum = Column (String(), primary_key=False, nullable=True)
    Lot = Column (String(), primary_key=False, nullable=True)
    Details = Column (String(), unique=False, nullable=True)
    Geraet = Column (String(), unique=False, nullable=True)

    def __init__(self, Anzahl, Artikelnummer, Bezeichnung, Ablaufdatum, Lot, Details, Geraet):
        self.Anzahl = Anzahl
        self.Artikelnummer = Artikelnummer
        self.Bezeichnung = Bezeichnung
        self.Ablaufdatum = Ablaufdatum
        self.Lot = Lot
        self.Details = Details
        self.Geraet = Geraet

    #def __repr__(self):
     #   return 'Anzahl{}', 'Artikelnummer{}', 'Bezeichnung={}', 'Ablaufdatum{}', 'Lot{}', 'Details={}', 'Gerät={}'\
      #        .format(self.Anzahl, self.Artikelnummer, self.Bezeichnung,  self.Ablaufdatum,  self.Lot, self.Details, self.Geraet)
        #return '<ErsatzteileKonrad%r>' % self.Anzahl
        #db.session.add()
        #db.session.commit()

#   ErsatzteileAlchemy_Bezeichnung = db.Column(Integer(), ForeignKey(ErsatzteileAlchemy.Bezeichnung))

@app.route('/kzb', methods = ['Get','POST'])
def insert_kzb():
    ersatzteile_konrad = ErsatzteileKonrad.query.all()

    if request.method == 'POST':
        Anzahl = request.form['Anzahl']
        Artikelnummer = request.form['Artikelnummer']
        Bezeichnung = request.form['Bezeichnung']
        Lot = request.form['Lot']
        Ablaufdatum = request.form['Ablaufdatum']
        Details = request.form['Details']
        Geraet = request.form['Geraet']

        Neue_ErsatzteileKonrad = ErsatzteileKonrad (Anzahl, Artikelnummer, Bezeichnung, Lot, Ablaufdatum, Details, Geraet)
        db.session.add(Neue_ErsatzteileKonrad)
        db.session.commit() 
        #flash('Record was successfully added')
        return redirect(url_for('kzb'))

    return render_template('kzb.html', ersatzteile_konrad = ersatzteile_konrad, title = 'kzb')

    #    ersatzteile-konrad = Anzahl = request.form['Anzahl'], request.form['Artikelnummer'], request.form['Bezeichnung'], request.form['Ablaufdatum'],
    #            request.form['Lot'], request.form['Details'], request.form['Geraet']    


@app.route('/ersatzteilliste')
def ersatzteilliste():
    Ersatzteile = ErsatzteileAlchemy.query.all()
    return render_template('ersatzteilliste.html', Ersatzteile = Ersatzteile, title = 'Ersatzteilliste')

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'admin' or request.form['password'] != 'admin':
            error = 'Invalid Credentials. Please try again.'
        else:
            return redirect(url_for('/login'))
    return render_template('login.html', error=error)    

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/eingang')
def eingang():
    return render_template('/eingang.html', title = 'Eingang')

@app.route('/carstock')
def carstock():
    return render_template('index.html')

@app.route('/bestellungen')
def bestellungen():
    Ersatzteile = ErsatzteileAlchemy.query.all()
    return render_template('bestellungen.html',Ersatzteile = Ersatzteile, title = 'Bestellungen')

@app.route('/ausgang')
def ausgang():
    return render_template('ausgang.html', title = 'Ausgang')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)