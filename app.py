import datetime
from flask import Flask, request, jsonify
from flask_restful import Api, Resource
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:906@localhost:5432/construction_works"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
ma = Marshmallow(app)


class Work(db.Model):
    __tablename__ = 'work'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    date_from = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    date_to = db.Column(db.DateTime)

    def __repr__(self):
        return f"Work(id = {self.id}, name = {self.name}, date_from = {self.date_from}, date_to = {self.date_to})"


class WorksVersion(db.Model):
    __tablename__ = 'works_versions'
    id = db.Column(db.Integer, primary_key=True)
    date_create = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    def __repr__(self):
        return f"Version(, date_create = {self.date_create})"


class WorksHistory(db.Model):
    __tablename__ = 'work_history'
    id = db.Column(db.Integer, primary_key=True)
    works_id = db.Column(db.Integer)
    name = db.Column(db.String(250), nullable=False)
    date_from = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    date_to = db.Column(db.DateTime)
    action = db.Column(db.String(10))
    version = db.Column(db.Integer, db.ForeignKey('works_versions.id'))

    def __repr__(self):
        return f"Work(id = {self.id},name = {self.name}, date_from = {self.date_from}, date_to = {self.date_to})"


class WorkSchema(ma.Schema):
    class Meta:
        fields = ("id", "name", "date_from", "date_to")


class VersionSchema(ma.Schema):
    class Meta:
        fields = ("id", "date_create")


work_schema = WorkSchema()
works_schema = WorkSchema(many=True)

version_schema = VersionSchema()
versions_schema = VersionSchema(many=True)


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


class VersionListResource(Resource):
    def get(self):
        versions = WorksVersion.query.all()
        return versions_schema.dump(versions)


class VersionResource(Resource):
    def get(self, version_id):
        WorksVersion.query.get_or_404(version_id)
        works = [{'id': u.id, 'name': u.name, 'date_from': u.date_from, 'date_to': u.date_to}
                 for u in Work.query.all()]

        if version_id == get_current_version():
            return jsonify(works)

        # Выполняем инверсионно операции до нужной версии
        history_works = WorksHistory.query.filter(WorksHistory.version >= version_id).all()
        history_works.reverse()
        for row in history_works:
            if row.action == 'delete':
                works += [{'id': row.works_id, 'name': row.name, 'date_from': row.date_from,
                           'date_to': row.date_to}]
                print(works)
            if row.action == 'insert':
                for u in works:
                    if u['id'] == row.works_id:
                        works.remove(u)
                        print(works)
            if row.action == 'update':
                for u in works:
                    if u['id'] == row.works_id:
                        u['name'] = row.name
                        u['date_from'] = row.date_from
                        u['date_to'] = row.date_to
                        print(works)
        return jsonify(works)


api.add_resource(WorkListResource, '/works')
api.add_resource(WorkResource, '/works/<int:work_id>')

api.add_resource(VersionListResource, '/versions')
api.add_resource(VersionResource, '/versions/<int:version_id>')

if __name__ == '__main__':
    app.run(debug=True)
