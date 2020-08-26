from flask import Flask, render_template, url_for, flash, redirect, request, jsonify, make_response, session, Response
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import select
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, inspect, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm.session import Session, sessionmaker
import datetime as dt
from sqlalchemy.dialects.postgresql import JSON
from flask_wtf import FlaskForm
from wtforms import SelectField, StringField, PasswordField, BooleanField,TextField, Form
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_bootstrap import Bootstrap
from wtforms.validators import InputRequired, Email, Length, DataRequired
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

# load config
app.config.from_pyfile('settings.py')

# setup libraries
bootstrap = Bootstrap(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(80))

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class LoginForm(FlaskForm):
    username = StringField('username', validators=[InputRequired(), Length(min=3, max=15)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=4, max=80)])
    remember = BooleanField('remember me')

class RegisterForm(FlaskForm):
    email = StringField('email', validators=[InputRequired(), Email(message='Invalid email'), Length(max=50)])
    username = StringField('username', validators=[InputRequired(), Length(min=3, max=15)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=4, max=80)])

class ErsatzteileAlchemy(db.Model):
    __tablename__ = 'ersatzteile_alchemy'
    Artikelnummer = Column(Integer(), unique=False) 
    Bezeichnung = Column(String(), unique=False, nullable=False)
    Details = Column(String(), unique=False, nullable=True)
    Geraet = Column(String(), unique=False, nullable=False)
    id = Column(Integer(), primary_key=True)

    def __init__(self, Artikelnummer, Bezeichnung, Details, Geraet):
        self.Artikelnummer = Artikelnummer
        self.Bezeichnung = Bezeichnung
        self.Details = Details
        self.Geraet = Geraet
#zom üebe:
#    def as_dict(self):
#        return {'Artikelnummer': self.Artikelnummer}

class ErsatzteileTechniker(db.Model):
    __tablename__ = 'ersatzteile_techniker'
    Techniker = Column(String(), nullable=False)
    Anzahl = Column(Integer(), primary_key = False, nullable=False)
    Artikelnummer = Column (Integer(), primary_key=False) 
    Bezeichnung = Column(String(), primary_key=False, unique=False)
    Lot = Column (Integer(), primary_key=False, unique=False, nullable=True)
    Ablaufdatum = Column (String(), primary_key=False, nullable=True)
    Details = Column (String(), unique=False, nullable=True)
    Geraet = Column (String(), unique=False, nullable=True)
    id = Column(Integer(), primary_key=True)

    def __init__(self, Techniker, Anzahl, Artikelnummer, Bezeichnung, Lot, Ablaufdatum, Details, Geraet):
        self.Techniker = Techniker
        self.Anzahl = Anzahl
        self.Artikelnummer = Artikelnummer
        self.Bezeichnung = Bezeichnung
        self.Lot = Lot
        self.Ablaufdatum = Ablaufdatum
        self.Details = Details
        self.Geraet = Geraet 

class ErsatzteileEingang(db.Model):
    __tablename__ = 'ersatzteile_eingang'
    Techniker = Column(String(), nullable=False)
    Datum = Column(String(), nullable=True)
    Anzahl = Column(Integer(), nullable=False)
    Artikelnummer = Column (Integer(), unique=False) 
    Bezeichnung = Column(String(),unique=False)
    Lot = Column (Integer(),unique=False, nullable=True)
    Ablaufdatum = Column (String(), nullable=True)
    Details = Column (String(), unique=False, nullable=True)
    Geraet = Column (String(), unique=False, nullable=True)
    id = Column(Integer(), primary_key=True)
    
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
    Anzahl = Column(Integer(),nullable=False)
    Artikelnummer = Column (Integer(),unique=False ) 
    Bezeichnung = Column(String(), unique=False)
    Lot = Column (Integer(),unique=False, nullable=True)
    Kunde = Column (String(), unique=False, nullable=True)
    SMR = Column(Integer(), unique=False, nullable=True)
    id = Column(Integer(), primary_key=True)

    def __init__(self, Techniker, Datum, Anzahl, Artikelnummer, Bezeichnung, Lot, Kunde, SMR):
        self.Techniker = Techniker
        self.Datum = Datum
        self.Anzahl = Anzahl
        self.Artikelnummer = Artikelnummer
        self.Bezeichnung = Bezeichnung
        self.Lot = Lot
        self.Kunde = Kunde
        self.SMR = SMR

class ErsatzteileBestellungen(db.Model):
    __tablename__ = 'ersatzteile_bestellungen'
    Techniker = Column(String(), nullable=False, unique=False)
    Bestelldatum = Column(String(), nullable=True, unique=False)
    Anzahl = Column(Integer(), nullable=False)
    Artikelnummer = Column (Integer(), unique=False) 
    Bezeichnung = Column(String(), unique=False, nullable=True)
    Details = Column (String(), unique=False, nullable=True)
    Geraet = Column (String(), unique=False, nullable=True)
    Erhalten_am = Column(String(), nullable=True, unique=False)
    id = Column(Integer(), primary_key=True)

    def __init__(self, Techniker, Bestelldatum, Anzahl, Artikelnummer, Bezeichnung, Details, Geraet, Erhalten_am):
        self.Techniker = Techniker
        self.Bestelldatum = Bestelldatum
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
    
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if check_password_hash(user.password, form.password.data):
                login_user(user, remember=form.remember.data)
                return redirect(url_for('index'))

        return '<h1>Ungültiger Benutzername oder falsches Passwort!</h1>'
        #return '<h1>' + form.username.data + ' ' + form.password.data + '</h1>'

    return render_template('login.html', form=form, title=login)

@app.route('/signup', methods=['GET', 'POST'])
@login_required  
def signup():  
    form = RegisterForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data, method='sha256')
        new_user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return '<h1>New user has been created!</h1>'
        #return '<h1>' + form.username.data + ' ' + form.email.data + ' ' + form.password.data + '</h1>'
    return render_template('signup.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/eingang', methods = ['Get','POST'])
@login_required
def eingang():
    ersatzteile_eingang = ErsatzteileEingang.query.all()
    return render_template('eingang.html', ersatzteile_eingang = ersatzteile_eingang, title = 'eingang')

@app.route('/eingang-insert', methods = ['Get','POST'])
@login_required
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

        Ersatzteil = ErsatzteileTechniker.query.filter_by(Artikelnummer = Artikelnummer, Techniker = Techniker, Lot = Lot).first()

        if Ersatzteil != None:
            #print(Ersatzteil.Artikelnummer)
            Anzahl = int(Ersatzteil.Anzahl) + int(Anzahl)
            delete_ErsatzteileTechniker = ErsatzteileTechniker.query.get(Ersatzteil.id)
            db.session.delete(delete_ErsatzteileTechniker)

        Neue_ErsatzteileTechniker = ErsatzteileTechniker (Techniker, Anzahl, Artikelnummer, Bezeichnung, Lot, Ablaufdatum, Details, Geraet)

        db.session.add(Neue_ErsatzteileTechniker)
        db.session.commit() 
        flash('Eintrag Erfolgreich.')
        return redirect(url_for('eingang'))  

@app.route('/ausgang')
@login_required
def ausgang():
    ersatzteile_ausgang = ErsatzteileAusgang.query.all()
    return render_template('ausgang.html', ersatzteile_ausgang = ersatzteile_ausgang, title = 'Ausgang')

@app.route('/ausgang-insert', methods = ['POST'])
@login_required
def insert_ausgang():
    if request.method == 'POST':
        Techniker = request.form['Techniker']
        Datum =  request.form['Datum']
        Anzahl = request.form['Anzahl']
        Artikelnummer = request.form['Artikelnummer']
        Bezeichnung = request.form['Bezeichnung']
        Lot = request.form['Lot']
        Kunde = request.form['Kunde']
        SMR = request.form['SMR']

        if Lot == '':
            Lot = None

        Neue_ErsatzteileAusgang = ErsatzteileAusgang (Techniker, Datum, Anzahl, Artikelnummer, Bezeichnung, Lot, Kunde, SMR)
        db.session.add(Neue_ErsatzteileAusgang)

        Ersatzteil = ErsatzteileTechniker.query.filter_by(Artikelnummer = Artikelnummer, Techniker = Techniker, Lot = Lot).first()

        if Ersatzteil != None:
            Anzahl = int(Ersatzteil.Anzahl) + int(Anzahl)
            Ersatzteil.Anzahl = Anzahl
            db.session.commit

        db.session.commit() 
        flash('Eintrag Erfolgreich.')
        return redirect(url_for('ausgang')) 

@app.route('/ausgang-update', methods = ['GET','POST'])   
@login_required
def update_ausgang():
    if request.method == 'POST':
        Update_ErsatzteileAusgang = ErsatzteileAusgang.query.get(request.form.get('id'))
        Update_ErsatzteileAusgang.Techniker = request.form['Techniker']
        Update_ErsatzteileAusgang.Datum = request.form['Datum']
        Update_ErsatzteileAusgang.Anzahl = request.form['Anzahl']
        Update_ErsatzteileAusgang.Artikelnummer = request.form['Artikelnummer']
        Update_ErsatzteileAusgang.Bezeichnung = request.form['Bezeichnung']
        Update_ErsatzteileAusgang.Lot = request.form['Lot']
        Update_ErsatzteileAusgang.Kunde = request.form['Kunde']
        Update_ErsatzteileAusgang.SMR = request.form['SMR']

        if Update_ErsatzteileAusgang.Lot == '':
            Update_ErsatzteileAusgang.Lot = None
        db.session.commit()
        flash("Update Erfolgreich.")
        return redirect(url_for('ausgang'))


@app.route('/eingang-update', methods = ['GET','POST'])   
@login_required
def update_eingang():
    if request.method == 'POST':
        Update_ErsatzteileEingang = ErsatzteileEingang.query.get(request.form.get('id'))
        Update_ErsatzteileEingang.Techniker = request.form['Techniker']
        Update_ErsatzteileEingang.Datum = request.form['Datum']
        Update_ErsatzteileEingang.Anzahl = request.form['Anzahl']
        Update_ErsatzteileEingang.Artikelnummer = request.form['Artikelnummer']
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
@login_required
def jwi():
    ersatzteile_jwi = ErsatzteileTechniker.query.filter_by(Techniker='JWI').all()
    return render_template('jwi.html', ersatzteile_jwi = ersatzteile_jwi, title = 'jwi')

@app.route('/kzb', methods = ['Get','POST'])
@login_required
def kzb():
    ersatzteile_kzb = ErsatzteileTechniker.query.filter_by(Techniker='KZB').all()
    return render_template('kzb.html', ersatzteile_kzb = ersatzteile_kzb, title = 'kzb')

@app.route('/kzb-insert', methods = ['POST'])
@login_required
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
@login_required  
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
@login_required
def delete_kzb(Artikelnummer):
    Delete_ErsatzteileKonrad = ErsatzteileKonrad.query.get(Artikelnummer)
    db.session.delete(Delete_ErsatzteileKonrad)
    db.session.commit()
    flash("Eintrag erfolgreich gelöscht.")
    return redirect(url_for('kzb'))

@app.route('/aka', methods = ['Get','POST'])
@login_required
def aka():
    ersatzteile_aka = ErsatzteileTechniker.query.filter_by(Techniker='AKA').all()
    return render_template('aka.html', ersatzteile_aka = ersatzteile_aka, title = 'aka')

@app.route('/ersatzteilliste')
@login_required
def ersatzteilliste():
    Ersatzteile = ErsatzteileAlchemy.query.all()
    return render_template('ersatzteilliste.html', Ersatzteile = Ersatzteile, title = 'Ersatzteilliste')

@app.route('/ersatzteilliste-insert', methods = ['POST'])
@login_required
def insert_ersatzteilliste():
    if request.method == 'POST':
        Artikelnummer = request.form['Artikelnummer']
        Bezeichnung = request.form['Bezeichnung']
        Details = request.form['Details']
        Geraet = request.form['Geraet']

        Neue_ErsatzteileAlchemy = ErsatzteileAlchemy (Artikelnummer, Bezeichnung, Details, Geraet)
        db.session.add(Neue_ErsatzteileAlchemy)
        db.session.commit() 
        flash('Eintrag Erfolgreich.')
        return redirect(url_for('ersatzteilliste'))  

@app.route('/ersatzteilliste-delete/<ID>/', methods = ['GET', 'POST'])
@login_required
def delete_liste(ID):
    Delete_ErsatzteileAlchemy = ErsatzteileAlchemy.query.get(ID)
    db.session.delete(Delete_ErsatzteileAlchemy)
    db.session.commit()
    return redirect(url_for('ersatzteilliste'))

@app.route('/', methods = ['Get'])
@login_required
def index():
    form = RegisterForm()
    current_user = User.query.filter_by(username='curent_user').all()
    return render_template('index.html', title = 'Index', form = form, current_user=current_user)

@app.route('/carstock', methods = ['Get','POST'])
@login_required
def techniker():
    ersatzteile_techniker = ErsatzteileTechniker.query.all()
    return render_template('carstock.html', ersatzteile_techniker = ersatzteile_techniker, title = 'Carstock-Techniker')


@app.route('/bestellungen', methods = ['GET','POST'])
@login_required
def bestellungen():
   # Ersatzteile = ErsatzteileAlchemy.query.filter_by(Artikelnummer='').all()Ersatzteile = Ersatzteile,
    ersatzteile_bestellungen = ErsatzteileBestellungen.query.all()
    return render_template('bestellungen.html', ersatzteile_bestellungen = ersatzteile_bestellungen, title = 'bestellungen')


@app.route('/bestellungen-insert', methods = ['GET','POST'])
@login_required
def insert_bestellungen():

    if request.method == 'POST':
        Techniker = request.form['Techniker']
        Bestelldatum = request.form['Bestelldatum']
        Anzahl = request.form['Anzahl']
        Artikelnummer = request.form['Artikelnummer']
        Bezeichnung = request.form['Bezeichnung']
        Details = request.form['Details']
        Geraet = request.form['Geraet']
        Erhalten_am = request.form['Erhalten_am']

        Neue_ErsatzteileBestellungen = ErsatzteileBestellungen (Techniker, Bestelldatum, Anzahl, Artikelnummer, Bezeichnung, Details, Geraet, Erhalten_am)
        db.session.add(Neue_ErsatzteileBestellungen)
        db.session.commit() 
        flash('Eintrag Erfolgreich.')
        return redirect(url_for('bestellungen'))  


@app.route('/bestellungen-update', methods = ['GET','POST'])  
@login_required 
def update_bestellungen():
    if request.method == 'POST':
        Update_Bestellungen = ErsatzteileBestellungen.query.get(request.form.get('id'))
        Update_Bestellungen.Techniker = request.form['Techniker']
        Update_Bestellungen.Bestelldatum = request.form['Bestelldatum']      
        Update_Bestellungen.Anzahl = request.form['Anzahl']
        Update_Bestellungen.Bezeichnung = request.form['Bezeichnung']
        Update_Bestellungen.Details = request.form['Details']
        Update_Bestellungen.Geraet = request.form['Geraet']
        Update_Bestellungen.Erhalten_am = request.form['Erhalten_am']
        db.session.commit()
        flash("Update Erfolgreich.")
        return redirect(url_for('bestellungen'))

@app.route('/delete_bestellungen/<id>/', methods = ['GET', 'POST'])
@login_required
def delete_bestellungen(id):
    Delete_Bestellungen = ErsatzteileBestellungen.query.get(id)
    db.session.delete(Delete_Bestellungen)
    db.session.commit()
    flash("Eintrag erfolgreich gelöscht.")
    return redirect(url_for('bestellungen'))

if __name__ == '__main__':
    app.run()