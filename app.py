
from flask import Flask, request, jsonify
from flask_restful import Resource, Api
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

DEPLOYMENT_ENVIRONMENT = 'local'

app = Flask(__name__)
api = Api(app)
if DEPLOYMENT_ENVIRONMENT == 'docker':
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////data/container.db'
elif DEPLOYMENT_ENVIRONMENT == 'local':
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
db = SQLAlchemy(app)
ma = Marshmallow(app)


class AppToBackendMapping(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    app_version = db.Column(db.String(20), unique=True, nullable=False)
    server_version = db.Column(db.String(20), unique=False, nullable=False)
    server_domain = db.Column(db.String(100), unique=False, nullable=False)

    def __repr__(self):
        return '<App Version: {app} | Server Version: {server} | Domain: {domain}>'.format(app=self.app_version, server=self.server_version, domain=self.server_domain)


class RuleSchema(ma.Schema):
    class Meta:
        # we want to expose:
        fields = ('app_version', 'server_version', 'server_domain')


rule_schema = RuleSchema()


def map_app_version_to_server_version(app_version = 'DEFAULT'):
    rule = AppToBackendMapping.query.filter_by(app_version=app_version).first()
    if rule is None:
        rule = AppToBackendMapping.query.filter_by(app_version='DEFAULT').first()
    return rule_schema.dump(rule).data, 200


class APIRouter(Resource):
    def get(self, app_version):
        return map_app_version_to_server_version(app_version=app_version)


api.add_resource(APIRouter, '/<string:app_version>')

if __name__ == '__main__':
    import migrate
    migrate.migrate_db()
    app.run(debug=True)
