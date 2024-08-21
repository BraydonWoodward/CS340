# animal_shelter.py
from pymongo import MongoClient
from pymongo.errors import PyMongoError
from bson.objectid import ObjectId

"""CRUD operations for Animal Collection in MongoDB"""
class AnimalShelter(object):

    def __init__(self, user, password, host, port, db, collection):
        # Initialize Connection with user-provided credentials
        try:
            self.client = MongoClient('mongodb://%s:%s@%s:%d' % (user, password, host, port), serverSelectionTimeoutMS=20000)
            self.database = self.client['%s' % db]
            self.collection = self.database['%s' % collection]
            print("Connection to MongoDB initialized successfully")
        except PyMongoError as e:
            print(f"Error initializing connection: {e}")


    def create(self, data):
        if data is not None:
            self.collection.insert_one(data)
            print("Document imported successfully")
        else:
            raise Exception("Data parameter is empty")


    def read(self, query):
        if query is not None:
            # Find document matching query
            cursor = self.collection.find(query)
            return list(cursor)
        else:
            print(f"No matching results to query: {query}")
            return []  # Return empty list
        
    def update(self, query, update_values, update_many = False):
        try:
            if update_many:
                result = self.collection.update_many(query, {'$set' : update_values})
            else: 
                result = self.collection.update_one(query, {'$set' : update_values})
            print(f"{result.modified_count} documents updated successfully.")
        except PyMongoError as e:
            print(f"An error occurred while updating documents: {e}")
            return 0
        
    def delete(self, query, delete_many = False):
        try: 
            if delete_many:
                result = self.collection.delete_many(query)
            else: 
                result = self.collection.delete_one(query)
            print(f"{result.deleted_count} documents successfully deleted")
        except PyMongoError as e:
            print(f"An error occurred while deleting documents: {e}")
            return 0