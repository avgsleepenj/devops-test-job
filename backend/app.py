import logging
import os
import re
import time
from urllib.parse import quote

from flask import Flask, jsonify, request
from pymongo import ASCENDING, MongoClient, UpdateOne
from pymongo.errors import PyMongoError

logging.basicConfig(
    level=os.getenv("LOG_LEVEL", "INFO"),
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
)
logger = logging.getLogger("shelter-api")


def env(name: str, default: str) -> str:
    """Return a non-empty environment value or a safe development default."""
    return os.getenv(name, default).strip() or default


mongo_host = env("HOST_DATABASE", "mongodb")
mongo_port = env("PORT_DATABASE", "27017")
mongo_db_name = env("NAME_DATABASE", "shelter")
mongo_username = quote(env("USERNAME_DATABASE", "root"), safe="")
mongo_password = quote(env("PASSWORD_DATABASE", "example"), safe="")
mongo_db_uri = quote(mongo_db_name, safe="")

mongo_uri = (
    f"mongodb://{mongo_username}:{mongo_password}@{mongo_host}:{mongo_port}/"
    f"{mongo_db_uri}?authSource=admin"
)

mongo_client = MongoClient(
    mongo_uri,
    serverSelectionTimeoutMS=3_000,
    connectTimeoutMS=3_000,
)
database = mongo_client[mongo_db_name]
cats_collection = database["cats"]

app = Flask(__name__)
app.json.ensure_ascii = False

CATS_DATA = [
    {
        "name": "Лисса",
        "age": 4,
        "breed": "Метис",
        "photo": "https://static3.vigbo.com/u6450/7603/photos/5973153/500-68f7324f82900065e606484887483196.jpg",
        "status": "ищет дом",
    },
    {
        "name": "Бетси",
        "age": 4,
        "breed": "Метис",
        "photo": "https://static3.vigbo.com/u6450/7603/photos/6073696/1000-46c45cd6622b2aa88b3448412ccbfbdf.jpg",
        "status": "ищет дом",
    },
    {
        "name": "Шемрок",
        "age": 4,
        "breed": "Метис",
        "photo": "https://static3.vigbo.com/u6450/7603/photos/5943356/500-a6e30a8e4bbcf07957dd359b69683b0f.jpg",
        "status": "ищет дом",
    },
    {
        "name": "Анфиса",
        "age": 4,
        "breed": "Метис",
        "photo": "https://static3.vigbo.com/u6450/7603/photos/5940592/1500-c2068da611e9469e6dc68a60880f8f58.JPG",
        "status": "ищет дом",
    },
    {
        "name": "Мурзилка",
        "age": 6,
        "breed": "Метис",
        "photo": "https://static3.vigbo.com/u6450/7603/photos/5973145/500-d75d61b7c15084001c7c652aeaae33eb.jpg",
        "status": "ищет дом",
    },
]


def initialize_database(retries: int = 15, delay_seconds: int = 2) -> None:
    """Wait for MongoDB and idempotently seed the initial cat records."""
    for attempt in range(1, retries + 1):
        try:
            mongo_client.admin.command("ping")
            cats_collection.create_index([("name", ASCENDING)], unique=True)
            operations = [
                UpdateOne(
                    {"name": cat["name"]},
                    {"$setOnInsert": cat},
                    upsert=True,
                )
                for cat in CATS_DATA
            ]
            result = cats_collection.bulk_write(operations, ordered=False)
            logger.info(
                "Database is ready; inserted %s initial records", result.upserted_count
            )
            return
        except PyMongoError as exc:
            if attempt == retries:
                logger.exception("MongoDB is unavailable after %s attempts", retries)
                raise RuntimeError("Could not initialize MongoDB") from exc
            logger.warning(
                "MongoDB is not ready (attempt %s/%s): %s",
                attempt,
                retries,
                exc,
            )
            time.sleep(delay_seconds)


def text_filter(value: str | None) -> dict[str, str] | None:
    """Create a safe, case-insensitive partial-match MongoDB filter."""
    if value is None:
        return None
    normalized = value.strip()
    if not normalized:
        return None
    if len(normalized) > 100:
        raise ValueError("Значение фильтра не должно быть длиннее 100 символов")
    return {"$regex": re.escape(normalized), "$options": "i"}


@app.get("/health")
def health():
    try:
        mongo_client.admin.command("ping")
    except PyMongoError:
        return jsonify({"status": "unhealthy"}), 503
    return jsonify({"status": "ok"})


@app.get("/api/cats")
def get_cats():
    query: dict[str, object] = {}

    try:
        age = request.args.get("age", "").strip()
        if age:
            parsed_age = int(age)
            if parsed_age < 0 or parsed_age > 40:
                raise ValueError("Возраст должен быть от 0 до 40")
            query["age"] = parsed_age

        for field in ("name", "breed", "status"):
            value = text_filter(request.args.get(field))
            if value:
                query[field] = value
    except ValueError as exc:
        return jsonify({"error": str(exc)}), 400

    try:
        cats = cats_collection.find(query, {"_id": 0}).sort("name", ASCENDING)
        return jsonify(list(cats))
    except PyMongoError:
        logger.exception("Could not read cats from MongoDB")
        return jsonify({"error": "База данных временно недоступна"}), 503


@app.errorhandler(404)
def not_found(_error):
    return jsonify({"error": "Маршрут не найден"}), 404


@app.errorhandler(500)
def internal_error(_error):
    logger.exception("Unhandled application error")
    return jsonify({"error": "Внутренняя ошибка сервера"}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8888)
