from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from pymongo import MongoClient
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
import os

app = Flask(__name__)

# MongoDB Connection (Replace with your MongoDB Atlas URI)
MONGO_URI = "mongodb+srv://user2003:2003user@mycluster.ccyu8.mongodb.net/?retryWrites=true&w=majority&appName=mycluster"
client = MongoClient(MONGO_URI)
db = client['template_db']

# JWT Configuration
app.config["JWT_SECRET_KEY"] = "supersecretkey"
jwt = JWTManager(app)

# Users Collection
users_collection = db['users']
templates_collection = db['templates']


# **1. Register User**
@app.route('/register', methods=['POST'])
def register():
    data = request.json
    if not data.get('email') or not data.get('password'):
        return jsonify({"msg": "Missing email or password"}), 400

    # Check if user already exists
    if users_collection.find_one({"email": data['email']}):
        return jsonify({"msg": "User already exists"}), 400

    # Hash password
    hashed_password = generate_password_hash(data['password'])
    
    # Save to DB
    user = {
        "first_name": data.get('first_name'),
        "last_name": data.get('last_name'),
        "email": data['email'],
        "password": hashed_password
    }
    users_collection.insert_one(user)

    return jsonify({"msg": "User registered successfully"}), 201


# **2. User Login**
@app.route('/login', methods=['POST'])
def login():
    data = request.json
    user = users_collection.find_one({"email": data.get('email')})

    if not user or not check_password_hash(user['password'], data.get('password')):
        return jsonify({"msg": "Invalid email or password"}), 401

    access_token = create_access_token(identity=str(user['_id']))
    return jsonify(access_token=access_token), 200


# **3. Insert New Template**
@app.route('/template', methods=['POST'])
@jwt_required()
def create_template():
    user_id = get_jwt_identity()
    data = request.json

    template = {
        "user_id": user_id,
        "template_name": data.get('template_name'),
        "subject": data.get('subject'),
        "body": data.get('body')
    }
    result = templates_collection.insert_one(template)
    
    return jsonify({"msg": "Template created", "id": str(result.inserted_id)}), 201


# **4. Get All Templates (Only User's Templates)**
@app.route('/template', methods=['GET'])
@jwt_required()
def get_templates():
    user_id = get_jwt_identity()
    templates = list(templates_collection.find({"user_id": user_id}))

    for template in templates:
        template["_id"] = str(template["_id"])

    return jsonify(templates), 200


# **5. Get Single Template by ID**
@app.route('/template/<template_id>', methods=['GET'])
@jwt_required()
def get_template(template_id):
    user_id = get_jwt_identity()
    template = templates_collection.find_one({"_id": ObjectId(template_id), "user_id": user_id})

    if not template:
        return jsonify({"msg": "Template not found"}), 404

    template["_id"] = str(template["_id"])
    return jsonify(template), 200


# **6. Update Single Template**
@app.route('/template/<template_id>', methods=['PUT'])
@jwt_required()
def update_template(template_id):
    user_id = get_jwt_identity()
    data = request.json

    result = templates_collection.update_one(
        {"_id": ObjectId(template_id), "user_id": user_id},
        {"$set": data}
    )

    if result.matched_count == 0:
        return jsonify({"msg": "Template not found or unauthorized"}), 404

    return jsonify({"msg": "Template updated"}), 200


# **7. Delete Single Template**
@app.route('/template/<template_id>', methods=['DELETE'])
@jwt_required()
def delete_template(template_id):
    user_id = get_jwt_identity()
    result = templates_collection.delete_one({"_id": ObjectId(template_id), "user_id": user_id})

    if result.deleted_count == 0:
        return jsonify({"msg": "Template not found or unauthorized"}), 404

    return jsonify({"msg": "Template deleted"}), 200


# if __name__ == '__main__':
#     app.run(debug=True)
