from flask import request, Response, Blueprint, json
import requests
from datetime import datetime
from time import mktime
from marshmallow import Schema, fields, pprint
from flask_sqlalchemy import SQLAlchemy

from models import Measurement, Gram
from serializers import measurement_schemas, gram_schemas
from extensions import db

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
    data = requests.get('https://cardiogr.am/heart/cardiograms/%s?no-cache=1' % (the_id)).json()

    line = data['cardiogram']['cards'][0]['song']['lines']['heartRate']['_line']
    slug = data['cardiogram']['vanityUrl']

    gram_exists = False if Gram.query.filter_by(slug=slug).count() == 0 else 1

    if not gram_exists:
      gram = Gram(slug=slug)
      status_msg = 'Nov Cardiogram shranjen.'
    else:
      gram = Gram.query.filter_by(slug=slug).first()
      ms = Measurement.query.with_parent(gram).all()
      for m in ms:
        m.delete()
      db.session.commit()

      status_msg = 'Cardiogram posodobljen.'
    
    for l in line:
      time = datetime.fromtimestamp(l['start'] / 1000)
      heart_rate = l['value']

      m = Measurement(time=time, heart_rate=heart_rate, gram=gram)
    
    db.session.add(gram)
    db.session.commit()
  
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