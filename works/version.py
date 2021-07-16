from works import db
from works.models.work import WorksVersion
from works.schemas.work import version_schema


def create_version():
    new_version = WorksVersion()
    db.session.add(new_version)
    db.session.commit()
    return version_schema.dump(new_version)


def get_current_version():
    if not WorksVersion.query.all():
        create_version()

    version = WorksVersion.query.order_by(WorksVersion.id.desc()).first()
    return version.id
