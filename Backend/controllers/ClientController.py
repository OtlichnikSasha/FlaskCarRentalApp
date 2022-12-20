from Backend.entities.Client import Client
from flask import Blueprint, request
from app_config import db
from Backend.utils import Utils
import math
client = Blueprint('client', __name__)

@client.route('/api/client/create', methods=['POST'])
def api_client_create():
    request_data = request.get_json()
    surname = request_data['surname'].strip()
    name = request_data['name'].strip()
    vu = request_data['vu']
    if len(str(vu)) != 6:
        return Utils.getError("Неверный формат водительского удостоверения")
    birthday = request_data['birthday']
    if len(str(birthday)) != 4:
        return Utils.getError("Неверный формат года рождения")
    phone = request_data['phone']
    if len(phone) != 18:
        return Utils.getError("Неверный формат номера телефона")
    phone = int(Utils.telephone(phone))
    client = Client(surname=surname, name=name, vu=vu, birthday=birthday, phone=phone)
    db.session.add(client)
    db.session.commit()
    return Utils.getAnswer({'client': client.as_dict()})

@client.route('/api/client/edit', methods=['POST'])
def api_client_edit():
    request_data = request.get_json()
    id = request_data['id']
    client = Client.query.filter_by(id=id).first()
    if client is None:
        return Utils.getError("Такого клиента не найдено!")
    surname = request_data['surname'].strip()
    name = request_data['name'].strip()
    vu = request_data['vu']
    if len(str(vu)) != 6:
        return Utils.getError("Неверный формат водительского удостоверения")
    birthday = request_data['birthday']
    if len(str(birthday)) != 4:
        return Utils.getError("Неверный формат года рождения")
    phone = request_data['phone']
    if len(phone) != 18:
        return Utils.getError("Неверный формат номера телефона")
    phone = int(Utils.telephone(phone))
    client.surname = surname
    client.name = name
    client.vu = vu
    client.birthday = birthday
    client.phone = phone
    db.session.commit()
    return Utils.getAnswer({'client': client.as_dict()})




@client.route('/api/client/remove')
def api_client_remove():
    id = request.values.get('id', 0, int)
    client = Client.query.filter_by(id=id).first()
    if client is None:
        return Utils.getError("Не найдено такого клиента!")
    db.session.delete(client)
    db.session.commit()
    return Utils.getAnswer({})

@client.route('/api/clients/get_all')
def api_clients_get_all():
    page = request.values.get('page', 0, int)
    item_count = page * 20
    skip_count = item_count - 20
    client = []
    clients = Client.query.order_by(Client.id.desc()).limit(
        item_count).offset(skip_count).all()
    for c in clients:
        client.append(c.as_dict())
    page_count = math.ceil((Client.query.count() / 20))
    return Utils.getAnswer({"clients": client, "page_count": page_count, 'page': page})


@client.route('/api/client/search')
def api_client_search():
    name = request.values.get('name', '', str).strip()
    client = []
    if name == '':
        client = Client.query.order_by(
        Client.id.desc()).all()
        return Utils.getAnswer({"clients": client})
    clients = Client.query.filter(Client.surname.contains(name)).order_by(
        Client.id.desc()).all()
    clients_name = Client.query.filter(Client.name.contains(name)).order_by(
        Client.id.desc()).all()
    clients_vu = Client.query.filter(Client.vu.contains(name)).order_by(
        Client.id.desc()).all()
    for c in clients:
        client.append(c.as_dict())
    for c in clients_name:
        client.append(c.as_dict())
    for c in clients_vu:
        client.append(c.as_dict())
    return Utils.getAnswer({"clients": client})