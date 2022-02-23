from crypt import methods
from distutils.log import debug
import json
from flask import Flask, request
from flask_pymongo import PyMongo
from bson.json_util import dumps
from bson.objectid import ObjectId
from flask import jsonify,request
import pymongo
from werkzeug.security import generate_password_hash, check_password_hash

#
UPLOAD_FOLDER = '/path/desktop/'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
app.secret_key = 'secretKey'

app.config['MONGO_URI'] = "mongodb+srv://iamkartiks:%40Arianna22@scientistai.xz2ub.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"

# app.config = ['UPLOAD_FOLDER'] = UPLOAD_FOLDER

mongo = PyMongo(app)

@app.route('/add', methods=['POST'])
def create_recipie():
    if request.method == 'POST':
        form = request.form
        _name = form.get('recipe_name')
        _ingredients=form.get('ingredients')
        _instructions = form.get('instructions')
        _items = request.form.getlist('items')
        # img = open(img_file, 'rb').read()
        # f = request.files['file']
        # f.save(secure_filename(f.filename))
        # return 'file uploaded successfully'

        _hashed_id = generate_password_hash(_name+'234')
        id = mongo.db.scientistAI.insert({'recipe_name':_name, 'ingredients':_ingredients, 'instructions':_instructions, 'items':_items})

        resp = jsonify(" Recipe Added Successfully ")

        resp.status_code = 200

        return resp



@app.route('/recipies')
def recipes():
    recipes = mongo.db.scientistAI.find()
    resp = dumps(recipes)
    return resp


@app.route('/recipies/<id>')
def recipe(id):
    recipe = mongo.db.scientistAI.find_one({'_id':ObjectId(id)})
    resp = dumps(recipe)
    return resp

@app.route('/delete/<id>', methods=['DELETE'])
def delete_recipe(id):
    mongo.db.scientistAI.delete_one({'id':ObjectId(id)})

    resp = jsonify("Recipe deleted successfully")

    resp.status_code = 200
    return resp


@app.route('/update/<id>', methods = ['PUT'])
def update_recipe(id):
    _id = id
    _json = request.json
    _name = _json['recipe_name']
    _ingredients = _json['ingredients']
    _instructions = _json['instructions']
    _items = request.form.getlist('items')

    if _id and request.method == 'PUT':
        # mongo.db.scientistAI.update_one({'_id':ObjectId(_id['$oid']) if '$oid' in _id else ObjectId(_id), {'$set:'}})
        pass


@app.errorhandler(404)
def not_found(error=None):
    message = {
        'status_code':404,
        'message': 'Not Found' + request.url
    }
    resp = jsonify(message)

    resp.status_code = 404

    return resp

if __name__ == "__main__":
    app.run(debug=True)

