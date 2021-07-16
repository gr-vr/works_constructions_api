import datetime

from works import db


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