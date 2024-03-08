from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash




class Restaurant:
    DB = "hotelschema"
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.description = data['description']
        self.user_id = data.get('user_id')
 

    @classmethod
    def create(cls, data):
        query = "INSERT INTO categories (name, description, price, image_path, user_id) VALUES (%(name)s, %(description)s, %(price)s, %(image_path)s, %(user_id)s);"
        return connectToMySQL(cls.DB).query_db(query, data)

    @classmethod
    def get_all(cls):
        query = "SELECT id, name, description, price, image_path, user_id FROM  categories;"
        results = connectToMySQL(cls.DB).query_db(query)
        categories = []
        if results:
            for category in results:
                categories.append(category)
        return categories
    
    
    





