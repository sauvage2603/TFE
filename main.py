from ast import Str
from turtle import update
from flask import Blueprint, redirect, render_template, Flask,request,flash
from flask_login import login_required, current_user
from . import db
from .models import Ticket, User, Reponse
import time
import stripe
stripe.api_key = 'sk_test_51JWwBZDkPiAcYfiPfeJMeIk6GIPsOJrbV6Osvo8BFHnYhAWFIsWMPWFk7pxpvmtHRDWXmF1Ho9ouLo1o4Oo35LzB009H1HyvH3'
YOUR_DOMAIN = 'http://localhost:5000/'
main = Blueprint('main', __name__)
#page index.html
@main.route('/',)
def index():
    db.create_all()
    return render_template("index.html")
@main.route('/profile')
@login_required
def profile():
    return render_template('profile.html', name=current_user.email, username=current_user.username)
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
    return render_template('ticket.html', name=current_user.email,id = current_user.id,tickets = Ticket.query.filter_by(user_id=current_user.id).order_by(Ticket.id.desc()))
@main.route('/voirticket',methods = ['GET', 'POST'])
@login_required
def voirticket():
    id_ticket = request.args.get('arg1')
    if request.method == 'POST':
        if not request.form['reponse']:
            flash('Veuillez renseigner tous les champs (sujet et objet)', 'error')
        else:
            reponse=Reponse(request.form["reponse"],current_user.username,request.form["id"])
            db.session.add(reponse)
            db.session.commit()
            return redirect('/voirticket?arg1='+str(request.form["id"]))
    if current_user.admin == "1":
        tickets=Ticket.query.filter_by(id=id_ticket)
    else:
        tickets=Ticket.query.filter_by(user_id=current_user.id).filter_by(id=id_ticket)
    return render_template('voirticket.html', name=current_user.email,id = current_user.id,tickets = tickets,id_ticket=id_ticket,reponses = Reponse.query.filter_by(id_reponse=id_ticket),admin=current_user.admin) 
@main.route('/dashboard')
@login_required
def dashboard():

    return render_template('dashboard.html')
@main.route('/ticketadmin',methods = ['GET', 'POST'])
@login_required
def ticketadmin():
    if current_user.admin =="1":
        etats=Ticket.query.filter_by()
        if request.method == 'POST':
            filtre = request.form["filtre-select"]
            if request.form["admin-select"] == "1":
                admin = "null"
            elif request.form["admin-select"] == "2":
                admin = current_user.username
            elif request.form["admin-select"] == "3":
                admin ="1"
            if admin == "1":
                if filtre != "4":
                    etats=Ticket.query.filter_by(etat=filtre)
                else:
                    etats=Ticket.query.filter_by()
            else:
                if filtre != "4":
                    etats=Ticket.query.filter_by(etat=filtre).filter_by(admin=admin)
                else:
                    etats=Ticket.query.filter_by(admin=admin)
    return render_template('ticketadmin.html',etats = etats)

@main.route('/shop')
@login_required
def shop():
    return render_template('shop.html')
@main.route('/buy_vip', methods = ['GET', 'POST'])
@login_required
def buy_vip():
    try:
        checkout_session = stripe.checkout.Session.create(
            line_items=[
                {
                    # Provide the exact Price ID (for example, pr_1234) of the product you want to sell
                    'price': 'price_1KRCZnDkPiAcYfiPmag885IE',
                    'quantity': 1,
                },
            ],
            mode='payment',
            success_url=YOUR_DOMAIN + 'successvip',
            cancel_url=YOUR_DOMAIN + 'shop',
        )
    except Exception as e:
        return str(e)
    
    return redirect(checkout_session.url, code=303)
@main.route('/close')
@login_required
def close():
    id_ticket = request.args.get('arg1')
    if current_user.admin=="1":
        update = Ticket.query.filter_by(id=id_ticket).first()
    else:
        update = Ticket.query.filter_by(user_id=current_user.id).filter_by(id=id_ticket).first()
    update.etat="3"
    db.session.merge(update)
    db.session.flush()
    db.session.commit()
    if request.args.get('arg2') == "admin" and current_user.admin=="1":
        return redirect('/ticketadmin')
    else:
        return redirect('/ticket')

@main.route('/test')
def test():
    return render_template('test.html')
@main.route('/successvip')
def successvip():
    return render_template('successvip.html')

@main.route('/priseticket')
@login_required
def priseticket():
    id_ticket = request.args.get('arg1')
    if current_user.admin=="1":
        update = Ticket.query.filter_by(id=id_ticket).first()
        update.admin=current_user.username
        update.etat="2"
        db.session.merge(update)
        db.session.flush()
        db.session.commit()
    return redirect('/voirticket?arg1='+id_ticket)
if __name__ == "__main__":
    main.run(ssl_context='adhoc')