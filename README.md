# works_constructions_api
REST API
/works:
GET - получение всех задач,
POST - добавление задачи:
{
  "name":"",
  "date_from":"",
  "date_to":"",
}
/works/<int:work_id> - Конкретная задача (GET - получение задачи, DELETE - удаление задачи, PATCH - изменение задачи)
/versions - GET получение всех версий списка
/versions/<int:version_id> - получение определенной версии списка
