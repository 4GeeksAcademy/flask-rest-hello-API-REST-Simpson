#creamos el archivo routes para poder generar los endpoints y
# que los usuarios puedan acceder a las rutas
from flask import Blueprint, jsonify
from models import User, Characters, Location

api = Blueprint("api", __name__)


# 1 GET all users
@api.route('/users', methods=['GET'])
def get_users():
    # obtener todos los usuarios de la familia 
    users = User.query.all()
    response = [user.serialize() for user in users] #
    return jsonify(response), 200

# get user for id 