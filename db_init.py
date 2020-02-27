from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db import Base, TodoItem

'''
Здесь у нас два шага: 
сначала создаем все нужные таблицы, 
потом наполняем базу данными. 
Делаем это, создавая объект класса TodoItem, добавляя его в сессию, 
и по окончанию всей процедуры - сохраняем сессию
(делаем commit).
'''
engine = create_engine("sqlite:///tasks.db", echo=True)
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
s = Session()
for desc in ("прочитать книгу", "учиться жонглировать 30 минут", "помыть посуду", "поесть"):
    t = TodoItem(desc)
    s.add(t)

s.commit()