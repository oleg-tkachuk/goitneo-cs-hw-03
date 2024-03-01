import os
import argparse
from dotenv import load_dotenv
from bson.objectid import ObjectId
from pymongo import MongoClient, errors
from pymongo.server_api import ServerApi


def create_cat(collection, name, age, features):
    try:
        new_cat = {
            "name": name,
            "age": age,
            "features": features
        }
        collection.insert_one(new_cat)
        print("[ok] New cat created.")
    except errors.PyMongoError as e:
        print("[error] MongoDB error:", e)


def read_cats(collection, cat_id=None, name=None):
    try:
        query = {}
        if cat_id:
            query["_id"] = ObjectId(cat_id)
        if name:
            query["name"] = name

        cats = collection.find(query)
        for cat in cats:
            print(cat)
    except errors.PyMongoError as e:
        print("[error] MongoDB error:", e)


def update_cat(collection, cat_id, name=None, age=None, features=None):
    try:
        query = {"_id": ObjectId(cat_id)}
        update_data = {}
        if name:
            update_data["name"] = name
        if age:
            update_data["age"] = age
        if features:
            update_data["features"] = features

        if update_data:
            collection.update_one(query, {'$set': update_data})
            print("[ok] Cat updated.")
        else:
            print("[info] No update data provided.")
    except errors.PyMongoError as e:
        print("MongoDB error:", e)


def delete_cat(collection, cat_id):
    try:
        result = collection.delete_one({"_id": ObjectId(cat_id)})
        if result.deleted_count:
            print("[ok] Cat deleted successfully")
        else:
            print("[info] Cat not found")
    except errors.PyMongoError as e:
        print("[error] MongoDB error:", e)


def delete_all_records(collection):
    try:
        result = collection.delete_many({})
        print(f"[ok] {result.deleted_count} records deleted.")
    except errors.PyMongoError as e:
        print("[error] MongoDB error:", e)


def cli():
    parser = argparse.ArgumentParser(
        description='Perform CRUD operations on cat database')
    parser.add_argument('--dotenv', type=str, default='.env',
                        help='Path to the .env file (default: %(default)s)')
    parser.add_argument('--action', required=True, type=str, help='Operation to perform',
                        choices=['create', 'read', 'update', 'delete', 'delete-all'])
    parser.add_argument('--id', type=str, help='The MongoDB ObjectId')
    parser.add_argument('--name', type=str, help='Name of the cat')
    parser.add_argument('--age', type=int, help='Age of the cat')
    parser.add_argument('--features', nargs='+',
                        help='List of features of the cat')

    return parser.parse_args()


def main():
    args = cli()

    load_dotenv(dotenv_path=args.dotenv)

    username = os.getenv('MONGO_INITDB_ROOT_USERNAME', 'root')
    password = os.getenv('MONGO_INITDB_ROOT_PASSWORD')
    hostname = os.getenv('MONGO_HOST', 'localhost')
    port = os.getenv('MONGO_PORT', '27017')
    auth_source = os.getenv('MONGO_AUTH_SOURCE', 'admin')
    mongo_db_name = os.getenv('MONGO_DB_NAME')
    mongo_collection_name = os.getenv('MONGO_COLLECTION_NAME')
    mongo_server_api_version = os.getenv('MONGO_SERVER_API_VERSION', '1')

    uri = f"mongodb://{username}:{password}@{
        hostname}:{port}/?authSource={auth_source}"
    client = MongoClient(uri, server_api=ServerApi(mongo_server_api_version))

    db = client[mongo_db_name]
    collection = db[mongo_collection_name]

    match args.action:
        case 'create':
            if args.name and args.age and args.features:
                create_cat(collection, args.name, args.age, args.features)
            else:
                print("[error] Missing required data for creation.")
        case 'read':
            read_cats(collection, cat_id=args.id, name=args.name)
        case 'update':
            if args.id:
                update_cat(collection, args.id, name=args.name,
                           age=args.age, features=args.features)
            else:
                print("[error] Missing cat's id for update.")
        case 'delete':
            if args.id:
                delete_cat(collection, args.id)
            else:
                print("[error] Missing cat's id for deletion.")
        case 'delete-all':
            delete_all_records(collection)
        case _:
            print("[error] Invalid or missing action.")


if __name__ == "__main__":
    main()
