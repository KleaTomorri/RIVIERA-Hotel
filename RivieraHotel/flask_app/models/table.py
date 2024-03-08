
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash


class Reservation:
    DB = "hotelschema"
    def __init__(self, data):
        self.id = data['id']
        self.date = data['date']
        self.time = data['time']
        self.firstName = data['firstName']
        self.lastName = data['lastName']
        self.emaiL = data['emaiL']
        self.created_at = data['created_at']
        
    @classmethod
    def create_table(cls, data):
        query = "INSERT INTO reservations (date, time, firstName, lastName, emaiL) VALUES (%(date)s, %(time)s, %(firstName)s, %(lastName)s, %(emaiL)s);"
        return connectToMySQL(cls.DB).query_db(query, data)