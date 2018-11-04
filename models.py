from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from extensions import db

class Measurement(db.Model):
  __tablename__ = 'measurements'

  id = db.Column(db.Integer, primary_key=True)
  time = db.Column(db.DateTime, nullable=True)
  heart_rate = db.Column(db.Integer)

  gram_id = db.Column(db.Integer, db.ForeignKey('gram.id'), nullable=False)
  gram = db.relationship('Gram', backref=db.backref('measurements', lazy=True))

  @staticmethod
  def get_all_measurements():
    return Measurement.query.all()

class Gram(db.Model):
  __tablename__ = 'gram'

  id = db.Column(db.Integer, primary_key=True)
  slug = db.Column(db.String(128), unique=True, nullable=False)

  def __repr__(self):
    return '<Gram %r>' % self.slug