import os
import time

import google
import pymysql.connections  # Aquí
from flask import Flask
from gcp_microservice_utils import setup_apigateway, setup_cloud_logging, setup_cloud_trace
from google.cloud.sql.connector import Connector  # type: ignore[attr-defined]
from sqlalchemy.exc import DatabaseError

from blueprints import BlueprintHealth
from containers import Container
from db import db


class FlaskMicroservice(Flask):
    container: Container


MAX_RETRIES = 5  # Define a constant for the maximum number of retries


def create_app(database_uri: str | None = None) -> FlaskMicroservice:
    if os.getenv('ENABLE_CLOUD_LOGGING') == '1':
        setup_cloud_logging()  # pragma: no cover

    app = FlaskMicroservice(__name__)
    app.container = Container()

    if os.getenv('ENABLE_CLOUD_TRACE') == '1':  # pragma: no cover
        setup_cloud_trace(app)

    setup_apigateway(app)

    # Register blueprints
    app.register_blueprint(BlueprintHealth)

    # SQLAlchemy configuration for Cloud SQL (MySQL) or SQLite
    if database_uri:
        app.config['SQLALCHEMY_DATABASE_URI'] = database_uri
    else:
        # Default configuration to use Google Cloud SQL with MySQL
        # Initialize Python Cloud SQL Connector object
        connector = Connector()

        credentials, _ = google.auth.default()  # type: ignore[no-untyped-call]
        credentials.refresh(request=google.auth.transport.requests.Request())  # type: ignore[no-untyped-call]
        cloudsql_user = credentials.service_account_email.replace('.gserviceaccount.com', '')
        cloudsql_instance = os.getenv('CLOUDSQL_INSTANCE')
        if not cloudsql_instance:
            raise ValueError('CLOUDSQL_INSTANCE environment variable must be set.')
        cloudsql_db = os.getenv('CLOUDSQL_DB')

        # Python Cloud SQL Connector database connection function
        def getconn() -> pymysql.connections.Connection:  # type: ignore[type-arg]
            return connector.connect(  # type: ignore[no-any-return]
                cloudsql_instance,
                'pymysql',  # Use pymysql to connect to MySQL
                db=cloudsql_db,
                user=cloudsql_user,
                enable_iam_auth=True,
            )

        app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://'
        app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
            'creator': getconn  # Use the custom connection function
        }

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize and create all tables in the database
    db.init_app(app)
    with app.app_context():
        retries = 0
        while True:
            try:
                db.create_all()
                break
            except DatabaseError:
                if retries < MAX_RETRIES:
                    retries += 1
                    time.sleep(1)
                    continue
                raise

    return app
