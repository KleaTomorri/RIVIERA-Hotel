from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re



class Category:
    DB = "hotelschema"
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.description = data['description']
        self.price = data['price']
        self.image_path = data['image_path']
        self.user_id = data.get('user_id')
    
    @classmethod
    def get_category_with_rooms(cls, category_id):
            query = "SELECT * FROM categories WHERE id = %(category_id)s;"
            data = {'category_id': category_id}
            result = connectToMySQL(cls.DB).query_db(query, data)
            if result:
                category_data = result[0]
                category = cls(category_data)
                category.rooms = Room.get_rooms_by_category_id(category_id)
                return category
            return None
        
        
        
        
        
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
    
    
    
    
    
    
    @classmethod
    def get_categories_by_id(cls, data):
        query = "SELECT * FROM categories LEFT JOIN users ON categories.user_id = users.id WHERE categories.id = %(id)s;"
        result = connectToMySQL(cls.DB).query_db(query, data)
        if result:
            return result[0]  # Return the first row of the result
        return None 

    @classmethod
    def deleteCategory(cls,data):
        query="DELETE FROM categories WHERE id=%(id)s;"
        return connectToMySQL(cls.DB).query_db(query,data)
    
    @classmethod
    def update(cls,data):
        query="UPDATE news SET name= %(name)s, description= %(description)s, price=%(price)s, image_path=%(image_path)s WHERE categories.id=%(id)s;"
        return connectToMySQL(cls.DB).query_db(query,data)
   

    #FEATURES
    @classmethod
    def insert_features(cls, data):
        query = "INSERT INTO feautures (name, category_id, user_id) VALUES (%(name)s,  %(category_id)s, %(user_id)s);"
        return connectToMySQL(cls.DB).query_db(query, data)
      
 
   
    @classmethod
    def get_features_by_category_id(cls, data):
        query = "SELECT * FROM feautures WHERE feautures.id = %(id)s"
        result = connectToMySQL(cls.DB).query_db(query, data)
        if result:
            return result[0]  # Return the first row of the result
        return False
    
    @classmethod
    def get_features_by_category_id(cls, category_id):
        query = "SELECT * FROM features WHERE category_id = %(category_id)s;"
        data = {'category_id': category_id}
        return connectToMySQL(cls.DB).query_db(query, data)

    
    
    @classmethod
    def update_action(cls, data):
        query = "UPDATE actions SET title = %(title)s, content = %(content)s, image = %(image)s WHERE id = %(id)s;"
        return connectToMySQL(cls.DB).query_db(query, data)
    
    @classmethod
    def delete_action(cls, data):
        query = "DELETE FROM actions WHERE id = %(id)s;"
        return connectToMySQL(cls.DB).query_db(query, data)
    
    
    
    #RESERVATIONS
     # Return a random number between 0 and 5

    

class Service:
    DB = "hotelschema"

    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.description = data['description']
        self.services_photo = data['services_photo']
        self.user_id = data['user_id']
       
     

    @classmethod
    def create(cls, data):
        query = "INSERT INTO services (name, description,  services_photo ,user_id ) VALUES (%(name)s, %(description)s,  %(services_photo)s, %(user_id)s);"
        return connectToMySQL(cls.DB).query_db(query, data)

    @classmethod
    def get_all(cls):
        query = "SELECT id, name, description, services_photo, user_id FROM services;"
        results = connectToMySQL(cls.DB).query_db(query)
        services = []
        if results:
            for row in results:
                service = {
                    'id': row['id'],
                    'name': row['name'],
                    'description': row['description'],
                    'services_photo': row['services_photo'],
                    'user_id': row['user_id']
                }
                services.append(service)
        return services


    @classmethod
    def get_service_by_id(cls, data):
        query = "SELECT * FROM services LEFT JOIN users ON services.user_id = users.id WHERE services.id = %(id)s;"
        result = connectToMySQL(cls.DB).query_db(query, data)
        if result:
            
            return result[0]
        return None

    @classmethod
    def deleteService(cls, data):
        query = "DELETE FROM services WHERE id=%(id)s;"
        return connectToMySQL(cls.DB).query_db(query, data)

    @classmethod
    def update(cls, data):
        query = "UPDATE events SET name= %(name)s, description= %(description)s WHERE events.id=%(id)s;"
        return connectToMySQL(cls.DB).query_db(query, data)


#ROOMS


class Room:
    DB = "hotelschema"
    def __init__(self, data):
        self.id = data['id']
        self.category_id = data['category_id']
        self.description = data['description']
        self.number = data['number']
        self.user_id = data['user_id']

    @classmethod
    def get_rooms_by_category_id(cls, category_id):
        query = "SELECT * FROM rooms WHERE category_id = %(category_id)s;"
        data = {'category_id': category_id}
        results = connectToMySQL(cls.DB).query_db(query, data)
        rooms = [Room(room_data) for room_data in results]
        return rooms
