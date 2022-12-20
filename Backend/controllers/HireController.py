from Backend.entities.Hire import Hire
from Backend.entities.Auto import Auto
from Backend.entities.Client import Client
from flask import Blueprint, request
from app_config import db
from Backend.utils import Utils
import math

hire = Blueprint('hire', __name__)


@hire.route('/api/hire/create')
def api_hire_create():
    auto_id = request.values.get("auto_id", 0, int)
    client_id = request.values.get("client_id", 0, int)
    сlient = Client.query.filter_by(id=client_id).first()
    if сlient is None:
        return Utils.getError("Такого клиента не найдено!")
    price = request.values.get('price', 0, int)
    start_date = request.values.get('start_date', '', str)
    end_date = request.values.get('end_date', '', str)
    hire = Hire(auto_id=auto_id, start_date=start_date, client_id=client_id, price=price, end_date=end_date)
    db.session.add(hire)
    db.session.commit()
    return Utils.getAnswer({})


@hire.route('/api/hire/remove')
def api_hire_remove():
    id = request.values.get('id', 0, int)
    hire = Hire.query.filter_by(id=id).first()
    if hire is None:
        return Utils.getError("Такой аренды не найдено")
    db.session.delete(hire)
    db.session.commit()
    return Utils.getAnswer({})
