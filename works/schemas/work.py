from works.extensions import ma


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
