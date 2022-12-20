import pymorphy2
import requests
import json
import logging
from flask import Response
from Backend.entities.Auto import Auto
from Backend.entities.Client import Client
from Backend.entities.Hire import Hire


import re

def getError(error_text):
    res = {
        'status': 'error',
        'message': error_text
    }
    return Response(
        response=json.dumps(res, ensure_ascii=False),
        mimetype='application/json',
        status=200
    )


def getAnswer(text, info=None):
    if info is None:
        info = {}
    res = {
        'status': 'ok',
        'message': text
    }
    answer = {**res, **info}
    return Response(
        response=json.dumps(answer, ensure_ascii=False, default=json_serial),
        mimetype='application/json',
        status=200
    )




def json_serial(obj):
    """JSON serializer for objects not serializable by default json code"""
    if isinstance(obj, Auto):
        return obj.__dict__
    elif isinstance(obj, Hire):
        return obj.__dict__
    elif isinstance(obj, Client):
        return obj.__dict__
    raise TypeError("Type %s not serializable" % type(obj))





def telephone(tel):
    pattern = r'(\+7|8|7).*?(\d{3}).*?(\d{3}).*?(\d{2}).*?(\d{2})'
    result = re.findall(pattern, tel)
    phone = ''
    z = 0
    for r in result[0]:
        if z != 0:
            phone += r
        z += 1
    return phone

