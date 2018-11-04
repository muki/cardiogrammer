from marshmallow import fields, Schema

class MeasurementSchema(Schema):
  id = fields.Int(dump_only=True)
  time = fields.DateTime(dump_only=True)
  heart_rate = fields.Int(dump_only=True)

measurement_schema = MeasurementSchema()
measurement_schemas = MeasurementSchema(many=True)