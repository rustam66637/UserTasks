# server.py
from bottle import route, run, static_file, view, redirect, request


class TodoItem:
    def __init__(self, description:str, unique_id:int):
        self.description = description
        self.is_completed = False
        self.uid = unique_id

    def __str__(self):
        return self.description.lower()

# Создаем dict для хранения всех задач
tasks_db = {
    1: TodoItem("прочитать книгу", 1),
    2: TodoItem("учиться жонглировать 30 минут", 2),
    3: TodoItem("помыть посуду", 3),
    4: TodoItem("поесть", 4),
}

###
@route("/static/<filename:path>")
def send_static(filename):
    return static_file(filename, root="static")


@route("/")
@view("index")
def index():
    # получаем значения словаря tasks_db
    tasks = tasks_db.values()
    return {"tasks": tasks}

@route("/api/delete/<uid:int>")
def api_delete(uid):
    tasks_db.pop(uid)
    # redirect переносит на указанный адрес
    return redirect("/")

@route("/api/complete/<uid:int>")
def api_complete(uid):
    tasks_db[uid].is_completed = True
    return 'OK'

@route("/add-task", method="POST")
def add_task():
    '''
    сохранить значение поля description в POST-запросе
    обрезать лишние пробелы (метод strip)
    если получившаяся строка не пуста, то:
    получить новый uid
    создать объект TodoItem с этим uid и этой строкой в качестве описания
    добавить новый объект в базу (словарь)
    '''
    desc = request.POST.description.strip()
    if len(desc) > 0:
        # новый uid -> max значение ключа + 1
        new_uid = max(tasks_db.keys()) + 1
        t = TodoItem(desc, new_uid)
        tasks_db[new_uid] = t
    return redirect("/")

###
run(host="localhost", port=8000, autoreload=True)
