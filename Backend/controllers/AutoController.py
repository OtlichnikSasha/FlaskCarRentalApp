from Backend.entities.Auto import Auto
from Backend.entities.Hire import Hire
from flask import Blueprint, request
from app_config import db
from Backend.utils import Utils
import math
auto = Blueprint('auto', __name__)

@auto.route('/api/auto/create', methods=['POST'])
def api_auto_create():
    request_data = request.get_json()
    mark = request_data['mark'].strip()
    model = request_data['model'].strip()
    vin = request_data['vin'].strip()
    issue_year = request_data['issue_year']
    gos_number = request_data['gos_number'].strip()
    color = request_data['color'].strip()
    price = request_data['price']
    if len(vin) != 17:
        return Utils.getError("Неверный формат вин номера!")
    if len(str(issue_year)) != 4:
        return Utils.getError("Неверный формат года выпуска!")
    if len(gos_number) != 6:
        return Utils.getError("Неверный формат гос номера!")
    auto = Auto(mark=mark, model=model, vin=vin, issue_year=issue_year, gos_number=gos_number,color=color, price=price)
    db.session.add(auto)
    db.session.commit()
    return Utils.getAnswer({'auto': auto.as_dict()})


@auto.route('/api/auto/remove')
def api_auto_remove():
    id = request.values.get("id", 0, int)
    auto = Auto.query.filter_by(id=id).first()
    if auto is None:
        return Utils.getError("Не найдено такого автомобиля!")
    db.session.delete(auto)
    db.session.commit()
    return Utils.getAnswer({"auto": 'Авто успешно удалено!'})

@auto.route('/api/auto/get_all')
def api_get_first_page_auto():
    page = 1
    item_count = page * 20
    skip_count = item_count - 20
    auto = []
    automobiles = Auto.query.order_by(Auto.id.desc()).limit(
        item_count).offset(skip_count).all()
    for a in automobiles:
        auto.append(a.as_dict())
    page_count = math.ceil((Auto.query.count() / 20))
    return Utils.getAnswer({"auto": auto, "page_count": page_count})


@auto.route('/api/auto/search')
def api_auto_search():
    name = request.values.get('name', '', str).strip()
    auto = []
    if name == '':
        auto = Auto.query.order_by(
        Auto.id.desc()).all()
        return Utils.getAnswer({"auto": auto})
    automobiles = Auto.query.filter(Auto.mark.contains(name)).order_by(
        Auto.id.desc()).all()
    automobiles_model = Auto.query.filter(Auto.model.contains(name)).order_by(
        Auto.id.desc()).all()
    automobiles_vin = Auto.query.filter(Auto.vin.contains(name)).order_by(
        Auto.id.desc()).all()
    for a in automobiles:
        auto.append(a.as_dict())
    for a in automobiles_model:
        auto.append(a.as_dict())
    for a in automobiles_vin:
        auto.append(a.as_dict())
    return Utils.getAnswer({"auto": auto})

@auto.route('/api/auto/search_for_hire')
def api_auto_search_for_hire():
    name = request.values.get('name', '', str).strip()
    auto = []
    if name == '':
        automobiles = Auto.query.order_by(
        Auto.id.desc()).all()
        for a in automobiles:
            availability = Hire.query.filter_by(auto_id=a.id).first()
            if availability is None:
                auto.append(a)
        return Utils.getAnswer({"auto": auto})
    automobiles = Auto.query.filter(Auto.mark.contains(name)).order_by(
        Auto.id.desc()).all()
    automobiles_model = Auto.query.filter(Auto.model.contains(name)).order_by(
        Auto.id.desc()).all()
    automobiles_vin = Auto.query.filter(Auto.vin.contains(name)).order_by(
        Auto.id.desc()).all()
    for a in automobiles:
        availability = Hire.query.filter_by(auto_id=a.id).first()
        if availability is None:
            auto.append(a.as_dict())
    for a in automobiles_model:
        availability = Hire.query.filter_by(auto_id=a.id).first()
        if availability is None:
            auto.append(a.as_dict())
    for a in automobiles_vin:
        availability = Hire.query.filter_by(auto_id=a.id).first()
        if availability is None:
            auto.append(a.as_dict())
    return Utils.getAnswer({"auto": auto})


@auto.route('/api/auto/get_by_id')
def api_auto_get_by_id():
    id = request.values.get('id', 0, int)
    auto = Auto.query.filter_by(id=id).first()
    if auto is None:
        return Utils.getError("Такого автомобиля не найдено!")
    return Utils.getAnswer({'auto': auto.as_dict()})
