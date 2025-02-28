from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
import datetime
from bson.objectid import ObjectId
import os

app = Flask(__name__)

# Configurations
app.config["MONGO_URI"] = "mongodb+srv://pop:1234pop5678@cluster0.j4mrj.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
app.config["JWT_SECRET_KEY"] = os.environ.get("pop", "1234pop5678")  # Change this to a secure secret key

# Initialize extensions
mongo = PyMongo(app)
jwt = JWTManager(app)

# User registration
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    first_name = data.get("first_name")
    last_name = data.get("last_name")
    email = data.get("email")
    password = data.get("password")

    if mongo.db.users.find_one({"email": email}):
        return jsonify({"msg": "User already exists"}), 400

    hashed_password = generate_password_hash(password, method='sha256')
    user = {
        "first_name": first_name,
        "last_name": last_name,
        "email": email,
        "password": hashed_password
    }

    mongo.db.users.insert_one(user)
    return jsonify({"msg": "User registered successfully"}), 201

# User login
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    user = mongo.db.users.find_one({"email": email})

    if not user or not check_password_hash(user["password"], password):
        return jsonify({"msg": "Invalid credentials"}), 401

    access_token = create_access_token(identity=str(user["_id"]), expires_delta=datetime.timedelta(hours=1))
    return jsonify(access_token=access_token), 200

# Protected route to create a new template
@app.route('/template', methods=['POST'])
@jwt_required()
def create_template():
    current_user_id = get_jwt_identity()
    data = request.get_json()

    template_name = data.get("template_name")
    subject = data.get("subject")
    body = data.get("body")

    if not template_name or not subject or not body:
        return jsonify({"msg": "Missing required fields"}), 400

    template = {
        "template_name": template_name,
        "subject": subject,
        "body": body,
        "user_id": current_user_id
    }

    mongo.db.templates.insert_one(template)
    return jsonify({"msg": "Template created successfully"}), 201

# Get all templates for the logged-in user
@app.route('/template', methods=['GET'])
@jwt_required()
def get_templates():
    current_user_id = get_jwt_identity()

    templates = mongo.db.templates.find({"user_id": current_user_id})
    templates_list = []
    for template in templates:
        template["_id"] = str(template["_id"])
        templates_list.append(template)

    return jsonify(templates=templates_list), 200

# Get a single template by ID
@app.route('/template/<template_id>', methods=['GET'])
@jwt_required()
def get_template(template_id):
    current_user_id = get_jwt_identity()

    template = mongo.db.templates.find_one({"_id": ObjectId(template_id), "user_id": current_user_id})

    if not template:
        return jsonify({"msg": "Template not found"}), 404

    template["_id"] = str(template["_id"])
    return jsonify(template), 200

# Update a template
@app.route('/template/<template_id>', methods=['PUT'])
@jwt_required()
def update_template(template_id):
    current_user_id = get_jwt_identity()
    data = request.get_json()

    template = mongo.db.templates.find_one({"_id": ObjectId(template_id), "user_id": current_user_id})

    if not template:
        return jsonify({"msg": "Template not found"}), 404

    updated_data = {key: value for key, value in data.items() if value}
    mongo.db.templates.update_one({"_id": ObjectId(template_id)}, {"$set": updated_data})

    return jsonify({"msg": "Template updated successfully"}), 200

# Delete a template
@app.route('/template/<template_id>', methods=['DELETE'])
@jwt_required()
def delete_template(template_id):
    current_user_id = get_jwt_identity()

    template = mongo.db.templates.find_one({"_id": ObjectId(template_id), "user_id": current_user_id})

    if not template:
        return jsonify({"msg": "Template not found"}), 404

    mongo.db.templates.delete_one({"_id": ObjectId(template_id)})
    return jsonify({"msg": "Template deleted successfully"}), 200

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
