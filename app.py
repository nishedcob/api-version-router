
from flask import Flask, request, jsonify
from flask_restful import Resource, Api
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from sqlalchemy.exc import IntegrityError

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
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
    db.create_all()
    def create_rule(app_version, server_version, server_domain):
        try:
            default_rule = AppToBackendMapping(app_version=app_version, server_version=server_version, server_domain=server_domain)
            db.session.add(default_rule)
            db.session.commit()
            print("Created Rule: {app} => {server} == {domain}".format(app=app_version, server=server_version, domain=server_domain))
        except IntegrityError:
            db.session.rollback()
            print("Rule Exists: {app} => {server} == {domain}".format(app=app_version, server=server_version, domain=server_domain))
    create_rule(app_version='DEFAULT', server_version='DEFAULT', server_domain='api.domain.com')
    create_rule(app_version='v1', server_version='v2', server_domain='apiv3.domain.com')
    create_rule(app_version='v2', server_version='v1', server_domain='apiv2.domain.com')
    create_rule(app_version='v3', server_version='v3', server_domain='apiv1.domain.com')
    app.run(debug=True)
