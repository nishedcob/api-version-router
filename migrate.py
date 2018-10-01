
from sqlalchemy.exc import IntegrityError

def migrate_db():
    import app
    app.db.create_all()
    def create_rule(app_version, server_version, server_domain):
        try:
            default_rule = app.AppToBackendMapping(app_version=app_version, server_version=server_version, server_domain=server_domain)
            app.db.session.add(default_rule)
            app.db.session.commit()
            print("Created Rule: {app} => {server} == {domain}".format(app=app_version, server=server_version, domain=server_domain))
        except IntegrityError:
            app.db.session.rollback()
            print("Rule Exists: {app} => {server} == {domain}".format(app=app_version, server=server_version, domain=server_domain))
    create_rule(app_version='DEFAULT', server_version='DEFAULT', server_domain='api.domain.com')
    create_rule(app_version='v1', server_version='v2', server_domain='apiv3.domain.com')
    create_rule(app_version='v2', server_version='v1', server_domain='apiv2.domain.com')
    create_rule(app_version='v3', server_version='v3', server_domain='apiv1.domain.com')

if __name__ == "__main__":
    migrate_db()
