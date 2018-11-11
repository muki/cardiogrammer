from marshmallow import fields, Schema

class GramSchema(Schema):
  id = fields.Int(dump_only=True)
  slug = fields.String(dump_only=True)
  url = fields.Function(lambda obj: 'https://cardiogr.am/c/%s?no-cache=1' % obj.slug)
  start = fields.DateTime(dump_only=True)
  end = fields.DateTime(dump_only=True)

gram_schema = GramSchema()
gram_schemas = GramSchema(many=True)

class MeasurementSchema(Schema):
  id = fields.Int(dump_only=True)
  time = fields.DateTime(dump_only=True)
  heart_rate = fields.Int(dump_only=True)
  gram = fields.Nested(GramSchema, dump_only=True)

measurement_schema = MeasurementSchema()
measurement_schemas = MeasurementSchema(many=True)