from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
from flask_cors import CORS
import logging, os
from logging import StreamHandler

# Параметры подключения
username = os.getenv('USERNAME_DATABASE')
password = os.getenv('PASSWORD_DATABASE')
host = "mongodb"  
port = os.getenv('PORT_DATABASE')
dbname = os.getenv('NAME_DATABASE')

# Строка подключения
connection_string = f"mongodb://{username}:{password}@{host}:{port}/{dbname}?authSource=admin"

app = Flask(__name__)
CORS(app)  # Инициализация CORS для всего приложения
app.config["MONGO_URI"] = connection_string
mongo = PyMongo(app)

# Настройка логирования
handler = StreamHandler()
handler.setLevel(logging.INFO)
app.logger.addHandler(handler)
app.logger.setLevel(logging.INFO)

cats_data = [
        { "name": "Лисса", "age": 4, "breed": "Метис", "photo": "https://static3.vigbo.com/u6450/7603/photos/5973153/500-68f7324f82900065e606484887483196.jpg", "status": "ищет дом" },
        { "name": "Бетси", "age": 4, "breed": "Метис", "photo": "https://static3.vigbo.com/u6450/7603/photos/6073696/1000-46c45cd6622b2aa88b3448412ccbfbdf.jpg", "status": "ищет дом" },
        { "name": "Шемрок", "age": 4, "breed": "Метис", "photo": "https://static3.vigbo.com/u6450/7603/photos/5943356/500-a6e30a8e4bbcf07957dd359b69683b0f.jpg", "status": "ищет дом" },
        { "name": "Анфиса", "age": 4, "breed": "Метис", "photo": "https://static3.vigbo.com/u6450/7603/photos/5940592/1500-c2068da611e9469e6dc68a60880f8f58.JPG", "status": "ищет дом" },
        { "name": "Мурзилка", "age": 6, "breed": "Метис", "photo": "https://static3.vigbo.com/u6450/7603/photos/5973145/500-d75d61b7c15084001c7c652aeaae33eb.jpg", "status": "ищет дом" }
    ]


def add_cats_to_db():
    cats_collection = mongo.db.cats
    for cat in cats_data:
        # Проверяем, существует ли уже такая запись
        if cats_collection.count_documents({"name": cat["name"]}) == 0:
            cats_collection.insert_one(cat)
            print(f"Добавлена кошка: {cat['name']}")
        else:
            print(f"Кошка {cat['name']} уже существует в базе данных.")


# Вызываем функцию добавления кошек в базу данных при старте скрипта
add_cats_to_db()


@app.route('/api/cats', methods=['GET'])
def get_cats():
    # Get filters from request parameters
    age = request.args.get('age')
    name = request.args.get('name')
    breed = request.args.get('breed')
    status = request.args.get('status')

    # Build query
    query = {}
    if age:
        query['age'] = int(age)
    if name:
        query['name'] = name
    if breed:
        query['breed'] = breed
    if status:
        query['status'] = status

    # Query the database
    cats = mongo.db.cats.find(query)

    # Convert to list of dicts
    cats_list = [{**cat, '_id': str(cat['_id'])} for cat in cats]

    return jsonify(cats_list)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8888)
