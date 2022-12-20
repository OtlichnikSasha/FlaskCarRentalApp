from flask import render_template
from app_config import app, db
from Backend.entities.Auto import Auto
from Backend.entities.Client import Client
from Backend.entities.Hire import Hire
from Backend.entities.Violations import Violations
from Backend.controllers.AutoController import auto
from Backend.controllers.ClientController import client
from Backend.controllers.HireController import hire
import math

app.register_blueprint(auto)
app.register_blueprint(client)
app.register_blueprint(hire)


db.create_all()

@app.route('/')
def index():
    auto_count = Auto.query.count()
    client_count = Client.query.count()
    hire_count = Hire.query.count()
    return render_template("index.html", auto_count=auto_count, client_count=client_count, hire_count=hire_count)


@app.route('/automobiles', defaults={'page': 1})
@app.route('/automobiles/<page>')
def automobiles(page):
    page = int(page)
    item_count = page * 20
    skip_count = item_count - 20
    automobiles = Auto.query.order_by(Auto.id.desc()).limit(
        item_count).offset(skip_count).all()
    page_count = math.ceil((Auto.query.count() / 20))
    return render_template("auto/automobiles.html", automobiles=automobiles, page_count=page_count, page=page)


@app.route('/auto/<id>')
def auto(id):
    auto = Auto.query.filter_by(id=id).first()
    return render_template("auto/auto.html", auto=auto)


@app.route('/createAuto')
def createAuto():
    return render_template("auto/createAuto.html")


@app.route('/clients', defaults={'page': 1})
@app.route('/clients/<page>')
def clients(page):
    page = int(page)
    item_count = page * 20
    skip_count = item_count - 20
    clients = Client.query.order_by(Client.id.desc()).limit(
        item_count).offset(skip_count).all()
    page_count = math.ceil((Client.query.count() / 20))
    return render_template("client/clients.html", clients=clients, page=page, page_count=page_count)


@app.route('/client/<id>')
def client(id):
    client = Client.query.filter_by(id=id).first()
    return render_template("client/client.html", client=client)


@app.route('/createClient')
def createClient():
    return render_template("client/createClient.html")


@app.route('/hires', defaults={'page': 1})
@app.route('/hires/<page>')
def hires(page):
    page = int(page)
    item_count = page * 20
    skip_count = item_count - 20
    hires = Hire.query.order_by(Hire.id.desc()).limit(
        item_count).offset(skip_count).all()
    for hire in hires:
        hire.auto = Auto.query.filter_by(id=hire.auto_id).first()
        hire.client = Client.query.filter_by(id=hire.client_id).first()
    page_count = math.ceil((Hire.query.count() / 20))
    return render_template("hire/hires.html", hires=hires, page_count=page_count, page=page)

@app.route('/createHire')
def createHire():
    auto = []
    automobiles = Auto.query.order_by(Auto.id.desc()).limit(10).all()
    for a in automobiles:
        availability = Hire.query.filter_by(auto_id=a.id).first()
        if availability is None:
            auto.append(a)
    clients = Client.query.order_by(Client.id.desc()).limit(10).all()
    return render_template("hire/startHire.html", automobiles=auto, clients=clients)

if __name__ == '__main__':
    app.run()
