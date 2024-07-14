"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

# create the jackson family object
jackson_family = FamilyStructure("Jackson")
member_one={"first_name": "Tommy", "age": 33, "lucky_numbers":[7, 13, 22]} 
member_two={"first_name": "Jane", "age": 35, "lucky_numbers":[10, 14, 3]} 
member_three={"first_name": "Jimmy", "age": 5, "lucky_numbers":[1]} 
jackson_family.add_member(member_one)
jackson_family.add_member(member_two)
jackson_family.add_member(member_three)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/members', methods=['GET'])
def handle_hello():
    # this is how you can use the Family datastructure by calling its methods
    members = jackson_family.get_all_members()
    response_body = members
    return jsonify(response_body), 200


@app.route('/member/<int:id>', methods=['GET'])
def get_member_by_id(id):
    try:
        member = jackson_family.get_member(id)
        if not member:
            return jsonify({"error": "Request member is missing"}), 200
        return jsonify(member), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/member', methods=['POST'])
def add_member():
    try:
        request_body = request.json
        if not request_body:
            return jsonify({"error": "Request body is missing"}), 400
        jackson_family.add_member(request_body)
        return jsonify({"message": "Member added successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/member/<int:id>', methods=['DELETE'])
def delete_member(id):
    try:
        member = jackson_family.get_member(id)
        if not member:
            return jsonify({"error": "Request id is missing"}), 200
        jackson_family.delete_member(id)
        return jsonify({"message": "Member deleted successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
        #
        # member = jackson_family.delete_member(id)
        # return jsonify(member), 200
        #


# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
