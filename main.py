from ast import Str
from flask import Blueprint, redirect, render_template, Flask,request,flash
from flask_login import login_required, current_user
from . import db
from .models import Ticket, User, Reponse
import time
main = Blueprint('main', __name__)
#page index.html
@main.route('/',)
def index():
    db.create_all()
    return render_template("index.html")
@main.route('/profile')
@login_required
def profile():
    return render_template('profile.html', name=current_user.name)
@main.route('/ticket',methods = ['GET', 'POST'])
@login_required
def ticket():
    if request.method == 'POST':
        if not request.form['sujet'] or not request.form['objet']:
            flash('Veuillez renseigner tous les champs (sujet et objet)', 'error')
        else:
            ticket=Ticket(request.form["sujet"],request.form["objet"],request.form["user_id"],"null","1"    )
            db.session.add(ticket)
            db.session.commit()
    return render_template('ticket.html', name=current_user.name,id = current_user.id,tickets = Ticket.query.filter_by(user_id=current_user.id).order_by(Ticket.id.desc()))
@main.route('/voirticket',methods = ['GET', 'POST'])
@login_required
def voirticket():
    id_ticket = request.args.get('arg1')
    if request.method == 'POST':
        if not request.form['reponse']:
            flash('Veuillez renseigner tous les champs (sujet et objet)', 'error')
        else:
            reponse=Reponse(request.form["reponse"],request.form["id"])
            db.session.add(reponse)
            db.session.commit()
            return redirect('/voirticket?arg1='+str(request.form["id"]))
    return render_template('voirticket.html', name=current_user.name,id = current_user.id,tickets = Ticket.query.filter_by(user_id=current_user.id).filter_by(id=id_ticket),id_ticket=id_ticket,reponses = Reponse.query.filter_by(id_reponse=id_ticket)) 
@main.route('/dashboard')
@login_required
def dashboard():

    return render_template('dashboard.html')
@main.route('/ticketadmin')
@login_required
def ticketadmin():

    return render_template('ticketadmin.html')