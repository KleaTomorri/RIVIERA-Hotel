from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash




class Review:
    DB = "hotelschema"
    def __init__(self, data):
        self.id = data['id']
        self.comment = data['comment']
        self.user_id = data.get('user_id')
 

    @classmethod
    def create(cls, data):
        query = "INSERT INTO comments (comment, user_id) VALUES (%(comment)s, %(user_id)s);"
        return connectToMySQL(cls.DB).query_db(query, data)

    # @classmethod
    # def get_all(cls, user_id=None):
    #     if user_id:
    #         query = "SELECT id, comment, user_id FROM comments WHERE user_id = %(user_id)s;"
    #         data = {'user_id': user_id}
    #     else:
    #         query = "SELECT id, comment, user_id FROM comments;"
    #         data = None

    #     results = connectToMySQL(cls.DB).query_db(query, data)
    #     reviews = []
    #     if results:
    #         for result in results:
    #             review = {
    #                 'id': result['id'],
    #                 'comment': result['comment'],
    #                 'user_id': result['user_id'],
    #                 # You may need to fetch the user's name here based on user_id
    #             }
    #             reviews.append(review)
    #     return reviews
    
    
    @classmethod
    def get_all(cls, user_id=None):
        if user_id:
            query = "SELECT comments.id, comments.comment, comments.user_id, users.first_name, users.last_name FROM comments JOIN users ON comments.user_id = users.id WHERE comments.user_id = %(user_id)s;"
            data = {'user_id': user_id}
        else:
            query = "SELECT comments.id, comments.comment, comments.user_id, users.first_name, users.last_name FROM comments JOIN users ON comments.user_id = users.id;"
            data = None

        results = connectToMySQL(cls.DB).query_db(query, data)
        reviews = []
        if results:
            for result in results:
                review = {
                    'id': result['id'],
                    'comment': result['comment'],
                    'user_id': result['user_id'],
                    'first_name': result['first_name'],
                    'last_name': result['last_name'],
                }
                reviews.append(review)
        return reviews


    
    
    @classmethod
    def update_comment(cls, data):
        query = "UPDATE comments set comment = %(comment)s where id = %(id)s;"
        return connectToMySQL(cls.db_name).query_db(query, data)
    
    @classmethod
    def delete_comment(cls, data):
        query = "DELETE FROM comments WHERE id = %(id)s;"
        return connectToMySQL(cls.DB).query_db(query, data)


    
    @classmethod
    def get_comment_by_id(cls, data):
        query = "SELECT * FROM comments WHERE id = %(id)s;"
        results = connectToMySQL(cls.DB).query_db(query, data)
        if results:
            return results[0]
        return None

    # @classmethod
    # def get_all(cls):
    #     query = "SELECT id, comment, user_id FROM comments;"
    #     results = connectToMySQL(cls.DB).query_db(query)
    #     reviews = []
    #     if results:
    #         for result in results:
    #             review = {
    #                 'id': result['id'],
    #                 'comment': result['comment'],
    #                 'user_id': result['user_id'],
    #                 # You may need to fetch the user's name here based on user_id
    #             }
    #             reviews.append(review)
    #     return reviews
