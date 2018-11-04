from flask import Flask, render_template
from extensions import db, migrate, cors

from config import app_config
from models import Measurement, Gram
from views import blueprint

def create_app(env_name):
  app = Flask(__name__)
  app.config.from_object(app_config[env_name])

  @app.route('/', methods=['GET'])
  def charts():
    return render_template('charts.html')

  register_extensions(app)
  register_blueprints(app)

  return app

def register_extensions(app):
  db.init_app(app)
  migrate.init_app(app, db)

def register_blueprints(app):
  db.init_app(app)
  migrate.init_app(app, db)
  app.register_blueprint(blueprint, url_prefix='')