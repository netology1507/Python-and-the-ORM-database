import os
import sqlalchemy
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import NoResultFound
from models import Publisher, Shop, Book, Stock, Sale

# Получение параметров подключения из переменных окружения
DB_USER = os.getenv('DB_USER', 'default_user')
DB_PASSWORD = os.getenv('DB_PASSWORD', 'default_password')
DB_NAME = os.getenv('DB_NAME', 'yourdatabase')
DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_PORT = os.getenv('DB_PORT', '5432')

# Формирование строки подключения
DSN = f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'

# Создание подключения к базе данных
engine = sqlalchemy.create_engine(DSN)
Session = sessionmaker(bind=engine)


def fetch_sales_by_publisher(publisher_identifier):
    session = Session()

    try:
        # Поиск издателя по имени или идентификатору
        if isinstance(publisher_identifier, str):
            publisher = session.query(Publisher).filter(Publisher.name == publisher_identifier).one()
        else:
            publisher = session.query(Publisher).filter(Publisher.id == publisher_identifier).one()

        # Запрос на выборку фактов покупки книг этого издателя
        sales_query = session.query(Book.title, Shop.name, Sale.price, Sale.date_sale) \
            .join(Stock, Book.id == Stock.id_book) \
            .join(Sale, Stock.id == Sale.id_stock) \
            .join(Shop, Stock.id_shop == Shop.id) \
            .filter(Book.id_publisher == publisher.id)

        sales = sales_query.all()

        # Вывод результатов
        for title, shop_name, price, date_sale in sales:
            print(f"{title} | {shop_name} | {price} | {date_sale}")
    except NoResultFound:
        print("Издатель не найден.")
    except Exception as e:
        print(f"Ошибка: {e}")
    finally:
        session.close()


if __name__ == '__main__':
    publisher_input = input("Введите имя или идентификатор издателя: ")
    try:
        publisher_input = int(publisher_input)  # Пытаемся интерпретировать ввод как ID
    except ValueError:
        pass  # Если не получается, оставляем как строку

    fetch_sales_by_publisher(publisher_input)
