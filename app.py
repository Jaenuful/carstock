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
app.config['SECRET_KEY'] = 'Jan123'
engine = create_engine('postgresql://postgres:root@localhost/carstock')
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:root@localhost/carstock'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)

class ErsatzteileAlchemy(db.Model):
    __tablename__ = 'ersatzteile_alchemy'
    Artikelnummer = Column (Integer(), primary_key=True) 
    Bezeichnung = Column (String(), unique=False, nullable=False)
    Details = Column (String(), unique=False, nullable=True)
    Geraet = Column (String(), unique=False, nullable=True)
#    ErsatzteileKonrad = db.relationship('ErsatzteileKonrad')

class ErsatzteileKonrad(db.Model):
    __tablename__ = 'ersatzteile_konrad'
    Anzahl = Column(Integer(), primary_key = False, nullable=False)
    Artikelnummer = Column (Integer(), primary_key=True) 
 #   Bezeichnung = input(f"ErsatzteileAlchemy for '{ersatzteile_alchemy.Bezeichnung}': $")
 #   Artikelnummer = db.realtionship('ErsatzteileAlchemy'), Column (Integer(), ForeignKey) 
    Bezeichnung = Column(String(), primary_key=False, unique=False)
    Lot = Column (Integer(), primary_key=False, unique=False, nullable=True)
    Ablaufdatum = Column (String(), primary_key=False, nullable=True)
    Details = Column (String(), unique=False, nullable=True)
    Geraet = Column (String(), unique=False, nullable=True)

    def __init__(self, Anzahl, Artikelnummer, Bezeichnung, Lot, Ablaufdatum, Details, Geraet):
        self.Anzahl = Anzahl
        self.Artikelnummer = Artikelnummer
        self.Bezeichnung = Bezeichnung
        self.Lot = Lot
        self.Ablaufdatum = Ablaufdatum
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
def kzb():
    ersatzteile_konrad = ErsatzteileKonrad.query.all()
    return render_template('kzb.html', ersatzteile_konrad = ersatzteile_konrad, title = 'kzb')

@app.route('/kzb-insert', methods = ['POST'])
def insert_kzb():
    if request.method == 'POST':
        Anzahl = request.form['Anzahl']
        Artikelnummer = request.form['Artikelnummer']
        Bezeichnung = request.form['Bezeichnung']
        Lot = request.form['Lot']
        Ablaufdatum = request.form['Ablaufdatum']
        Details = request.form['Details']
        Geraet = request.form['Geraet']

        if Lot == '':
            Lot = None

        Neue_ErsatzteileKonrad = ErsatzteileKonrad (Anzahl, Artikelnummer, Bezeichnung, Lot, Ablaufdatum, Details, Geraet)
        db.session.add(Neue_ErsatzteileKonrad)
        db.session.commit() 
        flash('Eintrag Erfolgreich')
        return redirect(url_for('kzb'))
    

@app.route('/kzb-update', methods = ['GET','POST'])   
def update_kzb():
    if request.method == 'POST':
        Update_ErsatzteileKonrad = ErsatzteileKonrad.query.get(request.form.get('Artikelnummer'))

        Update_ErsatzteileKonrad.Anzahl = request.form['Anzahl']
        Update_ErsatzteileKonrad.Bezeichnung = request.form['Bezeichnung']
        Update_ErsatzteileKonrad.Lot = request.form['Lot']
        Update_ErsatzteileKonrad.Ablaufdatum = request.form['Ablaufdatum']
        Update_ErsatzteileKonrad.Details = request.form['Details']
        Update_ErsatzteileKonrad.Geraet = request.form['Geraet']

        if Update_ErsatzteileKonrad.Lot == '':
            Update_ErsatzteileKonrad.Lot = None

        db.session.commit()
        flash("Update Erfolgreich")

        return redirect(url_for('kzb'))

@app.route('/kzb-delete/<Artikelnummer>/', methods = ['GET', 'POST'])
def delete_kzb(Artikelnummer):
    Delete_ErsatzteileKonrad = ErsatzteileKonrad.query.get(Artikelnummer)
    db.session.delete(Delete_ErsatzteileKonrad)
    db.session.commit()
    flash("Eintrag erfolgreich gelöscht")

    return redirect(url_for('kzb'))

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