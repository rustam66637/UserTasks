from bottle import route, run, static_file, view, redirect, request
from db import TodoItem
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

'''
Есть сессия, создаем ее с помощью «создателя сессий», который подключается к
базе (созданной как engine с помощью функции create_engine);
самое главное — это
путь к базе, в котором три прямые косые черты
'''
engine = create_engine("sqlite:///tasks.db")
Session = sessionmaker(bind=engine)
s = Session()


@route("/static/<filename:path>")
def send_static(filename):
    return static_file(filename, root="static")

'''
Любой запрос к коллекции тасок мы делаем с помощью query, и вообще это
один из двух режимов работы с SQLAlchemy, когда цепочка действий
вызывается подряд

После каждой операции по модификации таблицы (добавление или удаление из
нее строк) дергаем метод commit() на объекте сессии
'''

@route("/")
@view("index")
def index():
    tasks = s.query(TodoItem).order_by(TodoItem.uid)
    return {"tasks": tasks}


@route("/add-task", method="POST")
def add_task():
    desc = request.POST.description.strip()
    if len(desc) > 0:
        t = TodoItem(desc)
        s.add(t)
        s.commit()
    return redirect("/")


@route("/api/delete/<uid:int>")
def api_delete(uid):
    s.query(TodoItem).filter(TodoItem.uid == uid).delete()
    s.commit()
    return redirect("/")


@route("/api/complete/<uid:int>")
def api_complete(uid):
    t = s.query(TodoItem).filter(TodoItem.uid == uid).first()
    t.is_completed = True
    s.commit()
    return "Ok"

###
run(host="localhost", port=8080)
