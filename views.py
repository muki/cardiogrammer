from flask import request, Response, Blueprint, json, stream_with_context
import requests
from datetime import datetime
from time import mktime
from marshmallow import Schema, fields, pprint
from flask_sqlalchemy import SQLAlchemy

from models import Measurement, Gram
from serializers import measurement_schemas, gram_schemas
from extensions import db

from utils import updateGram

blueprint = Blueprint('measurements', __name__)

def json_response(res, status_code):
  return Response(
    mimetype="application/json",
    response=json.dumps(res),
    status=status_code
)

@blueprint.route('/inbound', methods=['GET'])
def twml():
  status_msg = 'SMS prejet, ampak potem je šlo nekaj narobe.'
  the_url = request.args.get('Body')
  the_id = the_url.split('/')[-1]

  if the_url:
    status_msg = updateGram(the_id)
  
  return Response('<Response><Message>%s</Message></Response>' % status_msg, mimetype='text/xml')

@blueprint.route('/data/', methods=['GET'])
def data():
  ms = Measurement.query.all()
  ms_data = measurement_schemas.dump(ms)
  return json_response(ms_data, 200)

@blueprint.route('/csv/', methods=['GET'])
def csv():
  the_csv = 'Time,Heart rate\n'
  ms = Measurement.query.all()

  for m in ms:
    the_csv += '%s,%d\n' % (m.time.isoformat(), m.heart_rate)

  return Response(the_csv, mimetype='text/csv')

@blueprint.route('/grams/', methods=['GET'])
def grams():
  gs = Gram.query.all()
  gs_data = gram_schemas.dump(gs)

  return json_response(gs_data, 200)

@blueprint.route('/grams/update/<slug>', methods=['GET'])
def update(slug):
  status_msg = updateGram(slug)

  return Response(status_msg, 200)

@blueprint.route('/grams/update/all', methods=['GET'])
def updateAll():
  gs = Gram.query.all()

  def generate():
    for i, g in enumerate(gs):
      status_msg = updateGram(g.slug)
      yield '<p>Updated gram %d of %d. | %s | %s</p>' % (i+1, len(gs), g.slug, status_msg)
  
  return Response(stream_with_context(generate()))

@blueprint.route('/grams/update/latest', methods=['GET'])
def updateLatest():
  gs = Gram.query.order_by('start desc').limit(1)
  if gs.count() > 0:
    status_msg = updateGram(gs[0].slug)
    return Response('%s | %s' % (gs[0].slug, status_msg))
  else:
    return Response('No grams here ...')