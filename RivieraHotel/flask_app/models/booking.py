from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash




class   Booking:
    DB = "hotelschema"
    def __init__(self, data):
        self.id = data['id']
        self.checkin = data['name']
        self.checkout = data['description']
        self.num_children = data['price']
        self.num_adults = data['image_path']
        self.user_id = data.get('user_id')
        self.payment_id= data.get('payment_id')
        self.category_id = data.get('category_id')
        self.room_id = data.get('room_id')


    @classmethod
    def create(cls, data):
        query = "INSERT INTO bookings (checkin, checkout, num_children, num_adults, user_id, payment_id, category_id, room_id) VALUES (%(checkin)s, %(checkout)s, %(num_children)s, %(num_adults)s, %(user_id)s, %(payment_id)s, %(category_id)s, %(room_id)s);"
        return connectToMySQL(cls.DB).query_db(query, data)
    

    @classmethod
    def check_availability(cls, checkin, checkout):
        query = '''
            SELECT * 
            FROM rooms 
            WHERE id NOT IN (
                SELECT room_id 
                FROM bookings 
                WHERE %(checkin)s < checkout 
                AND %(checkout)s > checkin
            );
        '''
        query = query % {'checkin': checkin, 'checkout': checkout}  # Replace placeholders with actual values
        results = connectToMySQL(cls.DB).query_db(query)
        return results

