import os

from flask import Flask
from gcp_microservice_utils import cloudsql_mysql_getconn, setup_apigateway, setup_cloud_logging, setup_cloud_trace

from blueprints import BlueprintHealth
from containers import Container
from db import db


class FlaskMicroservice(Flask):
    container: Container


def create_app(database_uri: str | None = None) -> FlaskMicroservice:
    if os.getenv('ENABLE_CLOUD_LOGGING') == '1':
        setup_cloud_logging()  # pragma: no cover

    app = FlaskMicroservice(__name__)
    app.container = Container()

    if os.getenv('ENABLE_CLOUD_TRACE') == '1':  # pragma: no cover
        setup_cloud_trace(app)

    setup_apigateway(app)

    # SQLAlchemy configuration for Cloud SQL (MySQL) or SQLite
    if database_uri:  # pragma: no cover
        app.config['SQLALCHEMY_DATABASE_URI'] = database_uri
    else:  # pragma: no cover
        app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://'
        app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
            'creator': cloudsql_mysql_getconn(
                instance=os.environ['CLOUDSQL_INSTANCE'],
                database=os.environ['CLOUDSQL_DB'],
            )
        }

    db.init_app(app)

    app.register_blueprint(BlueprintHealth)

    return app
