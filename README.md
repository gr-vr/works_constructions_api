# works_constructions_api
REST API <br>
/works:<br>
GET - получение всех задач,<br>
POST - добавление задачи:<br>
{<br>
  "name":"",<br>
  "date_from":"",<br>
  "date_to":"",<br>
}<br>
/works/<int:work_id> - Конкретная задача (GET - получение задачи, DELETE - удаление задачи, PATCH - изменение задачи)<br>
/versions - GET получение всех версий списка<br>
/versions/<int:version_id> - получение определенной версии списка<br>
