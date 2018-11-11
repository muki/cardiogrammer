import requests
from datetime import datetime

from models import Measurement, Gram
from extensions import db

def updateGram(slug):
  data = requests.get('https://cardiogr.am/heart/cardiograms/%s?no-cache=1' % slug).json()

  line = data['cardiogram']['cards'][0]['song']['lines']['heartRate']['_line']
  slug = data['cardiogram']['vanityUrl']
  start = data['cardiogram']['start']
  end = data['cardiogram']['end']

  gram_exists = False if Gram.query.filter_by(slug=slug).count() == 0 else 1

  if not gram_exists:
    gram = Gram(slug=slug, start=datetime.fromtimestamp(start / 1000), end=datetime.fromtimestamp(end / 1000))
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

  return status_msg