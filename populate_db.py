import os
import json
import sqlalchemy
from sqlalchemy.orm import sessionmaker
from models import Base, Publisher, Shop, Book, Stock, Sale

# Получение параметров подключения из переменных окружения
DB_USER = os.getenv('DB_USER', 'postgres')
DB_PASSWORD = os.getenv('DB_PASSWORD', 'postgres')
DB_NAME = os.getenv('DB_NAME', 'bookstore')
DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_PORT = os.getenv('DB_PORT', '5432')

# Формирование строки подключения
DSN = f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'

# Создание подключения к базе данных
engine = sqlalchemy.create_engine(DSN)
Base.metadata.create_all(engine)

# Создание сессии для работы с базой данных
Session = sessionmaker(bind=engine)
session = Session()

# Чтение данных из JSON-файла
with open('tests_data.json', 'r', encoding='utf-8') as fd:
    data = json.load(fd)

# Заполнение базы данных данными из файла
for record in data:
    model = {
        'publisher': Publisher,
        'shop': Shop,
        'book': Book,
        'stock': Stock,
        'sale': Sale,
    }[record.get('model')]

    # Создаем экземпляр модели и добавляем его в сессию
    session.add(model(id=record.get('pk'), **record.get('fields')))

# Сохранение изменений в базе данных
session.commit()

# Закрытие сессии
session.close()

print("База данных успешно заполнена тестовыми данными.")

