from flask import request
from flask_restful import Resource

from works import db
from works.models.work import Work, WorksHistory
from works.schemas.work import work_schema
from works.version import get_current_version, create_version


class WorkListResource(Resource):
    def get(self):
        works = Work.query.all()
        return works_schema.dump(works)

    def post(self):
        new_work = Work(
            name=request.json['name'],
            date_from=request.json['date_from'],
            date_to=request.json['date_to']
        )

        db.session.add(new_work)
        db.session.commit()

        history_work = WorksHistory(
            works_id=new_work.id,
            name=request.json['name'],
            date_from=request.json['date_from'],
            date_to=request.json['date_to'],
            action='insert',
            version=get_current_version()
        )

        db.session.add(history_work)
        db.session.commit()
        create_version()
        return work_schema.dump(new_work)


class WorkResource(Resource):
    def get(self, work_id):
        work = Work.query.get_or_404(work_id)
        return work_schema.dump(work)

    def patch(self, work_id):
        work = Work.query.get_or_404(work_id)
        history_work = WorksHistory(
            works_id=work.id,
            name=work.name,
            date_from=work.date_from,
            date_to=work.date_to,
            action='update',
            version=get_current_version()
        )
        db.session.add(history_work)

        if 'name' in request.json:
            work.name = request.json['name']
        if 'date_from' in request.json:
            work.date_from = request.json['date_from']
        if 'date_to' in request.json:
            work.date_to = request.json['date_to']

        db.session.commit()
        create_version()
        return work_schema.dump(work)

    def delete(self, work_id):
        work = Work.query.get_or_404(work_id)
        work_history = WorksHistory(
            works_id=work.id,
            name=work.name,
            date_from=work.date_from,
            date_to=work.date_to,
            action='delete',
            version=get_current_version()
        )
        db.session.add(work_history)
        db.session.delete(work)
        db.session.commit()
        create_version()
        return '', 204
