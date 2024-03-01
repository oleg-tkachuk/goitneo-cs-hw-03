import argparse
from bson.objectid import ObjectId
from pymongo import MongoClient, errors
from pymongo.server_api import ServerApi


uri = "mongodb://localhost:27017"
client = MongoClient(uri, server_api=ServerApi('1'))

db = client['cats_db']
collection = db['cats']


def create_cat(name, age, features):
    try:
        new_cat = {
            "name": name,
            "age": age,
            "features": features
        }
        collection.insert_one(new_cat)
        print("New cat created.")
    except errors.PyMongoError as e:
        print("MongoDB error:", e)


def read_cats(cat_id=None, name=None):
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
        print("MongoDB error:", e)


def update_cat(cat_id, name=None, age=None, features=None):
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
            print("Cat updated.")
        else:
            print("No update data provided.")
    except errors.PyMongoError as e:
        print("MongoDB error:", e)


def delete_cat(cat_id):
    try:
        result = collection.delete_one({"_id": ObjectId(cat_id)})
        if result.deleted_count:
            print("Cat deleted successfully")
        else:
            print("Cat not found")
    except errors.PyMongoError as e:
        print("MongoDB error:", e)


def main():
    parser = argparse.ArgumentParser(
        description='Perform CRUD operations on cat database')
    parser.add_argument('--action', type=str, help='Operation to perform',
                        choices=['create', 'read', 'update', 'delete'])
    parser.add_argument('--id', type=str, help='The MongoDB ObjectId')
    parser.add_argument('--name', type=str, help='Name of the cat')
    parser.add_argument('--age', type=int, help='Age of the cat')
    parser.add_argument('--features', nargs='+',
                        help='List of features of the cat')

    args = parser.parse_args()

    match args.action:
        case 'create':
            if args.name and args.age and args.features:
                create_cat(args.name, args.age, args.features)
            else:
                print("Missing required data for creation.")
        case 'read':
            read_cats(cat_id=args.id, name=args.name)
        case 'update':
            if args.id:
                update_cat(args.id, name=args.name,
                           age=args.age, features=args.features)
            else:
                print("Missing cat's id for update.")
        case 'delete':
            if args.id:
                delete_cat(args.id)
            else:
                print("Missing cat's id for deletion.")
        case _:
            print("Invalid or missing action.")


if __name__ == "__main__":
    main()
