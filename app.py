from flask import Flask, render_template, url_for, flash, redirect, request, jsonify, make_response
from forms import LoginForm
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
from flask_login import LoginManager

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Jan123'
engine = create_engine('postgresql://postgres:root@localhost/carstock')
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:root@localhost/carstock'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)
#login = LoginManager(app)

class ErsatzteileAlchemy(db.Model):
    __tablename__ = 'ersatzteile_alchemy'
    ID = Column(Integer(), primary_key=True)
    Artikelnummer = Column (Integer(), unique=False) 
    Bezeichnung = Column (String(), unique=False, nullable=False)
    Details = Column (String(), unique=False, nullable=True)
    Geraet = Column (String(), unique=False, nullable=True)
#    ErsatzteileKonrad = db.relationship('ErsatzteileKonrad')

class ErsatzteileTechniker(db.Model):
    __tablename__ = 'ersatzteile_techniker'
    Techniker = Column(String(), nullable=False)
    Anzahl = Column(Integer(), primary_key = False, nullable=False)
    Artikelnummer = Column (Integer(), primary_key=True) 
 #   Bezeichnung = input(f"ErsatzteileAlchemy for '{ersatzteile_alchemy.Bezeichnung}': $")
 #   Artikelnummer = db.realtionship('ErsatzteileAlchemy'), Column (Integer(), ForeignKey) 
    Bezeichnung = Column(String(), primary_key=False, unique=False)
    Lot = Column (Integer(), primary_key=False, unique=False, nullable=True)
    Ablaufdatum = Column (String(), primary_key=False, nullable=True)
    Details = Column (String(), unique=False, nullable=True)
    Geraet = Column (String(), unique=False, nullable=True)

class ErsatzteileEingang(db.Model):
    __tablename__ = 'ersatzteile_eingang'
    Techniker = Column(String(), nullable=False)
    Datum = Column(String(), nullable=True)
    Anzahl = Column(Integer(), primary_key = False, nullable=False)
    Artikelnummer = Column (Integer(), primary_key=True) 
    Bezeichnung = Column(String(), primary_key=False, unique=False)
    Lot = Column (Integer(), primary_key=False, unique=False, nullable=True)
    Ablaufdatum = Column (String(), primary_key=False, nullable=True)
    Details = Column (String(), unique=False, nullable=True)
    Geraet = Column (String(), unique=False, nullable=True)
    def __init__(self, Techniker, Datum, Anzahl, Artikelnummer, Bezeichnung, Lot, Ablaufdatum, Details, Geraet):
        self.Techniker = Techniker
        self.Datum = Datum
        self.Anzahl = Anzahl
        self.Artikelnummer = Artikelnummer
        self.Bezeichnung = Bezeichnung
        self.Lot = Lot
        self.Ablaufdatum = Ablaufdatum
        self.Details = Details
        self.Geraet = Geraet   

class ErsatzteileAusgang(db.Model):
    __tablename__ = 'ersatzteile_ausgang'
    Techniker = Column(String(), nullable=False)
    Datum = Column(String(), nullable=True)
    Anzahl = Column(Integer(), primary_key = False, nullable=False)
    Artikelnummer = Column (Integer(), primary_key=True) 
    Bezeichnung = Column(String(), primary_key=False, unique=False)
    Lot = Column (Integer(), primary_key=False, unique=False, nullable=True)
    def __init__(self, Techniker, Datum, Anzahl, Artikelnummer, Bezeichnung, Lot):
        self.Techniker = Techniker
        self.Datum = Datum
        self.Anzahl = Anzahl
        self.Artikelnummer = Artikelnummer
        self.Bezeichnung = Bezeichnung
        self.Lot = Lot

class ErsatzteileBestellungen(db.Model):
    __tablename__ = 'ersatzteile_bestellungen'
    Bestelldatum = Column(String(), nullable=True, unique=False)
    Techniker = Column(String(), nullable=False)
    Anzahl = Column(Integer(), primary_key = False, nullable=False)
    Artikelnummer = Column (Integer(), primary_key=True) 
    Bezeichnung = Column(String(), primary_key=False, unique=False)
    Details = Column (String(), unique=False, nullable=True)
    Geraet = Column (String(), unique=False, nullable=True)
    Erhalten_am = Column(String(), nullable=True, unique=False)
    def __init__(self, Bestelldatum, Techniker, Datum, Anzahl, Artikelnummer, Bezeichnung, Details, Geraet, Erhalten_am):
        self.Bestelldatum = Bestelldatum
        self.Techniker = Techniker
        self.Anzahl = Anzahl
        self.Artikelnummer = Artikelnummer
        self.Bezeichnung = Bezeichnung  
        self.Details = Details
        self.Geraet = Geraet 
        self.Erhalten_am = Erhalten_am

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
    

#   ErsatzteileAlchemy_Bezeichnung = db.Column(Integer(), ForeignKey(ErsatzteileAlchemy.Bezeichnung))

@app.route('/login', methods=['GET', 'POST'])
def login():
#    if current_user.is_authenticated:
#        return redirect(url_for('index'))
#    form = LoginForm()
#    if form.validate_on_submit():
#        user = User.query.filter_by(username=form.username.data).first()
#        if user is None or not user.check_password(form.password.data):
 #           flash('Invalid username or password')
  #          return redirect(url_for('login'))
   #     login_user(user, remember=form.remember_me.data)
    #    return redirect(url_for('index'))
    return render_template('login.html', title='WebCarstock-Login') #form=form)


@app.route('/eingang', methods = ['Get','POST'])
def eingang():
    ersatzteile_eingang = ErsatzteileEingang.query.all()
    return render_template('eingang.html', ersatzteile_eingang = ersatzteile_eingang, title = 'eingang')

@app.route('/eingang-insert', methods = ['POST'])
def insert_eingang():
    if request.method == 'POST':
        Techniker = request.form['Techniker']
        Datum =  request.form['Datum']
        Anzahl = request.form['Anzahl']
        Artikelnummer = request.form['Artikelnummer']
        Bezeichnung = request.form['Bezeichnung']
        Lot = request.form['Lot']
        Ablaufdatum = request.form['Ablaufdatum']
        Details = request.form['Details']
        Geraet = request.form['Geraet']

        if Lot == '':
            Lot = None

        Neue_ErsatzteileEingang = ErsatzteileEingang (Techniker, Datum, Anzahl, Artikelnummer, Bezeichnung, Lot, Ablaufdatum, Details, Geraet)
        db.session.add(Neue_ErsatzteileEingang)
        db.session.commit() 
        flash('Eintrag Erfolgreich.')
        return redirect(url_for('eingang'))  

@app.route('/eingang-update', methods = ['GET','POST'])   
def update_eingang():
    if request.method == 'POST':
        Update_ErsatzteileEingang = ErsatzteileEingang.query.get(request.form.get('Artikelnummer'))
        Update_ErsatzteileEingang.Anzahl = request.form['Techniker']
        Update_ErsatzteileEingang.Datum = request.form['Datum']
        Update_ErsatzteileEingang.Anzahl = request.form['Anzahl']
        Update_ErsatzteileEingang.Bezeichnung = request.form['Bezeichnung']
        Update_ErsatzteileEingang.Lot = request.form['Lot']
        Update_ErsatzteileEingang.Ablaufdatum = request.form['Ablaufdatum']
        Update_ErsatzteileEingang.Details = request.form['Details']
        Update_ErsatzteileEingang.Geraet = request.form['Geraet']

        if Update_ErsatzteileEingang.Lot == '':
            Update_ErsatzteileEingang.Lot = None
        db.session.commit()
        flash("Update Erfolgreich.")
        return redirect(url_for('eingang'))

@app.route('/jwi', methods = ['Get','POST'])
def jwi():
    ersatzteile_jwi = ErsatzteileTechniker.query.filter_by(Techniker='JWI').all()
    return render_template('jwi.html', ersatzteile_jwi = ersatzteile_jwi, title = 'jwi')


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
        flash('Eintrag Erfolgreich.')
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
        flash("Update Erfolgreich.")
        return redirect(url_for('kzb'))

@app.route('/kzb-delete/<Artikelnummer>/', methods = ['GET', 'POST'])
def delete_kzb(Artikelnummer):
    Delete_ErsatzteileKonrad = ErsatzteileKonrad.query.get(Artikelnummer)
    db.session.delete(Delete_ErsatzteileKonrad)
    db.session.commit()
    flash("Eintrag erfolgreich gelöscht.")
    return redirect(url_for('kzb'))

@app.route('/aka', methods = ['Get','POST'])
def aka():
    ersatzteile_aka = ErsatzteileTechniker.query.filter_by(Techniker='AKA').all()
    return render_template('aka.html', ersatzteile_aka = ersatzteile_aka, title = 'aka')

@app.route('/ersatzteilliste')
def ersatzteilliste():
    Ersatzteile = ErsatzteileAlchemy.query.all()
    return render_template('ersatzteilliste.html', Ersatzteile = Ersatzteile, title = 'Ersatzteilliste')

@app.route('/ersatzteilliste-delete/<ID>/', methods = ['GET', 'POST'])
def delete_liste(ID):
    Delete_ErsatzteileAlchemy = ErsatzteileAlchemy.query.get(ID)
    db.session.delete(Delete_ErsatzteileAlchemy)
    db.session.commit()
    return redirect(url_for('ersatzteilliste'))

@app.route('/')
def index():
    return render_template('index.html', title = 'Index')

@app.route('/carstock', methods = ['Get','POST'])
def techniker():
    ersatzteile_techniker = ErsatzteileTechniker.query.all()
    return render_template('carstock.html', ersatzteile_techniker = ersatzteile_techniker, title = 'Carstock-Techniker')


@app.route('/bestellungen', methods = ['Get','POST'])
def bestellungen():
    ersatzteile_bestellungen = ErsatzteileBestellungen.query.all()
    return render_template('bestellungen.html', ersatzteile_bestellungen = ersatzteile_bestellungen, title = 'bestellungen')


@app.route('/bestellungen-insert', methods = ['POST'])
def insert_bestellungen():
    if request.method == 'POST':
        Bestelldatum = request.form['Bestelldatum']
        Anzahl = request.form['Anzahl']
        Artikelnummer = request.form['Artikelnummer']
        Bezeichnung = request.form['Bezeichnung']
        Details = request.form['Details']
        Geraet = request.form['Geraet']
        Erhalten_am = request.form['Erhalten am']
        Neue_Bestellungen = ErsatzteileBestellungen (Bestelldatum, Anzahl, Artikelnummer, Bezeichnung, Details, Geraet, Erhalten_am)
        db.session.add(Neue_Bestellungen)
        db.session.commit() 
        flash('Eintrag Erfolgreich.')
        return redirect(url_for('bestellungen'))  

@app.route('/bestellungen-update', methods = ['GET','POST'])   
def update_bestellungen():
    if request.method == 'POST':
        Update_Bestellungen = ErsatzteileBestellungen.query.get(request.form.get('Artikelnummer'))
        Update_Bestellungen.Bestelldatum = request.form['Bestelldatum']
        Update_Bestellungen.Anzahl = request.form['Anzahl']
        Update_Bestellungen.Bezeichnung = request.form['Bezeichnung']
        Update_Bestellungen.Details = request.form['Details']
        Update_Bestellungen.Geraet = request.form['Geraet']
        Update_Bestellungen.Erhalten_am = request.form['Erhalten am']
        db.session.commit()
        flash("Update Erfolgreich.")
        return redirect(url_for('bestellungen'))

@app.route('/bestellungen-delete/<Artikelnummer>/', methods = ['GET', 'POST'])
def delete_bestellungen(Artikelnummer):
    Delete_Bestellungen = ErsatzteileBestellungen.query.get(Artikelnummer)
    db.session.delete(Delete_Bestellungen)
    db.session.commit()
    flash("Eintrag erfolgreich gelöscht.")
    return redirect(url_for('bestellungen'))

@app.route('/ausgang')
def ausgang():
    ersatzteile_ausgang = ErsatzteileAusgang.query.all()
    return render_template('ausgang.html', ersatzteile_ausgang = ersatzteile_ausgang, title = 'Ausgang')

@app.route('/ausgang-insert', methods = ['POST'])
def insert_ausgang():
    if request.method == 'POST':
        Techniker = request.form['Techniker']
        Datum =  request.form['Datum']
        Anzahl = request.form['Anzahl']
        Artikelnummer = request.form['Artikelnummer']
        Bezeichnung = request.form['Bezeichnung']
        Lot = request.form['Lot']

        if Lot == '':
            Lot = None

        Neue_ErsatzteileAusgang = ErsatzteileAusgang (Techniker, Datum, Anzahl, Artikelnummer, Bezeichnung, Lot)
        db.session.add(Neue_ErsatzteileAusgang)
        db.session.commit() 
        flash('Eintrag Erfolgreich.')
        return redirect(url_for('ausgang')) 

@app.route('/ausgang-update', methods = ['GET','POST'])   
def update_ausgang():
    if request.method == 'POST':
        Update_ErsatzteileAusgang = ErsatzteileAusgang.query.get(request.form.get('Artikelnummer'))
        Update_ErsatzteileAusgang.Anzahl = request.form['Techniker']
        Update_ErsatzteileAusgang.Datum = request.form['Datum']
        Update_ErsatzteileAusgang.Anzahl = request.form['Anzahl']
        Update_ErsatzteileAusgang.Bezeichnung = request.form['Bezeichnung']
        Update_ErsatzteileAusgang.Lot = request.form['Lot']

        if Update_ErsatzteileAusgang.Lot == '':
            Update_ErsatzteileAusgang.Lot = None
        db.session.commit()
        flash("Update Erfolgreich.")
        return redirect(url_for('ausgang'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)