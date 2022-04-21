from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import recipe
from flask_app.models import user

class Recipe:
    db_name = 'cookbook'
    def __init__(self,data):
        self.id = data['id']
        self.user_id = data['user_id']
        self.name = data['name']
        self.under_30 = data["under_30"]
        self.description = data['description']
        self.instructions = data['instructions']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']


    @classmethod
    def delete(cls,data):
        query = "DELETE FROM recipes WHERE id = %(id)s"
        return connectToMySQL(cls.db_name).query_db(query,data)

    @classmethod
    def get_recipes(cls,data):
        query = "SELECT * FROM recipes WHERE user_id=%(user_id)s"
        return connectToMySQL(cls.db_name).query_db(query,data)

    @classmethod
    def get_recipe(cls,data):
        query = "SELECT * FROM recipes WHERE id = %(id)s"
        recipe = connectToMySQL(cls.db_name).query_db(query,data)
        return cls(recipe[0])

    @classmethod
    def save_recipe(cls,data):
        query = "INSERT INTO recipes ( name, description, instructions, under_30, user_id,created_at, updated_at ) VALUES (  %(name)s, %(description)s, %(instructions)s,%(under_30)s, %(user_id)s, NOW(),NOW() )"
        return connectToMySQL(cls.db_name).query_db(query,data)

    @classmethod
    def update(cls,data):
        query = "UPDATE recipes SET  name=%(name)s, under_30=%(under_30)s, description=%(description)s, instructions=%(instructions)s, created_at= %(created_at)s, updated_at=%(updated_at)s WHERE id=%(id)s"
        return connectToMySQL(cls.db_name).query_db(query,data)

    @staticmethod
    def validate_recipe(recipe):        
        is_valid = True
        if len(recipe["name"]) < 3:
            flash("Name of the recipe must be longer than 3 characters.")
            is_valid = False
        if "under_30" not in recipe:
            flash("You have to choose yes or no.")
            is_valid = False
        if len(recipe["description"]) < 3:
            flash("Description must be longer than 3 characters.")
            is_valid = False
        if len(recipe["instructions"]) < 3:
            flash("Your instrustions must be longer than 3 characters")
            is_valid = False
        if len(recipe["created_at"]) < 1:
            flash("You need to choose a date.")
            is_valid = False
        return is_valid