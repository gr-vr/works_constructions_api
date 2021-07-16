from flask import jsonify
from flask_restful import Resource

from works.models.work import WorksVersion, Work, WorksHistory
from works.schemas.work import versions_schema
from works.version import get_current_version


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