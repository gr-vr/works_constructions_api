from flask import Flask

from .extensions import db, api
from .resources.version import VersionListResource, VersionResource
from .resources.work import WorkListResource, WorkResource


def create_app(config_file='settings.py'):
    app = Flask(__name__)

    app.config.from_pyfile('settings.py')

    db.init_app(app)

    api.add_resource(WorkListResource, '/works')
    api.add_resource(WorkResource, '/works/<int:work_id>')

    api.add_resource(VersionListResource, '/versions')
    api.add_resource(VersionResource, '/versions/<int:version_id>')

    return app
