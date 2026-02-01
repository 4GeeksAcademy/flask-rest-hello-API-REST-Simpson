#creamos el archivo routes para poder generar los endpoints y
# que los usuarios puedan acceder a las rutas
from flask import Blueprint, jsonify, request
from models import db, User, Characters, Location

api = Blueprint("api", __name__)


# 1 GET all users
@api.route('/users', methods=['GET'])
def get_users():
   
    users = User.query.all()
    response = [user.serialize() for user in users] #
    return jsonify(response), 200



# get characters all
@api.route('/characters', methods=['GET'])
def get_characters():
   
    characters = Characters.query.all()
    response = [character.serialize() for character in characters] #
    return jsonify(response), 200


# get characters for id en vez de people
@api.route('/characters/<int:id>', methods=['GET'])
def get_characters_id(id):

    characters = Characters.query.get(id)

    if not characters:
        return jsonify({"error": "Not found"}), 404
    return jsonify(characters.serialize()), 200


# GET locations all
@api.route('/locations', methods=['GET'])
def get_locations():
   
    locations = Location.query.all()
    response = [location.serialize() for location in locations] #
    return jsonify(response), 200


# GET locations for id
@api.route('/locations/<int:id>', methods=['GET'])
def get_locations_id(id):

    locations = Location.query.get(id)

    if not locations:
        return jsonify({"error": "Not found"}), 404
    return jsonify(locations.serialize()), 200



# GET todos los favoritos del USUARIO
@api.route('/users/<int:user_id>/favorites', methods=['GET'])
def get_user_favorites(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    

    characters = [char.serialize() for char in user.favorite_characters]
    locations = [loc.serialize() for loc in user.favorite_locations]

    return jsonify({
        "favorite_characters": characters,
        "favorites_locations": locations
    }), 200



# POST agregar un nuevo registro o usuario a la lista
@api.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    if not data.get('email') or not data.get('password') or not data.get ('name'):
        return jsonify({"error": "name, email and password is required"}), 400
# Ahora insertamos la funcion para un nuevo usuario     
    new_user = User(
        name = data ["name"],
        email = data ["email"],
        password = data ["password"],
        is_active = True
        
        
    )

    db.session.add(new_user)
    # Ahora hacemos COMMIT y lo guardamos en la base de datos
    db.session.commit()
    return jsonify (new_user.serialize()), 201 # 201 significa que la solicitud al servidor fue exitosa y, 
#como resultado, se ha creado un nuevo recurso


# POST Agregar personajes favoritos por id
@api.route('/favorite/character/<int:character_id>', methods=['POST'])
def add_favorite_character(character_id):
    data = request.get_json()
    user_id = data.get("user_id")


    user = User.query.get(user_id)
    character = Characters.query.get(character_id)


    if not user or not character:
        return jsonify({"error": "User or Character not found"}), 404
    
# agregar el personaje a la base
    user.favorite_characters.append(character)
    db.session.commit()

    return jsonify({"message": f"Character {character.name} added to favorites"}), 201


# POST Agregar lugares favoritos por id
@api.route('/favorite/location/<int:location_id>', methods=['POST'])
def add_favorite_location(location_id):
    data = request.get_json()
    user_id = data.get ("user_id")


    user = User.query.get(user_id)
    location = Location.query.get(location_id)

    if not user or not location: 
        return jsonify({"error": "User or Location not found"}), 404
    
    user.favorite_locations.append(location)
    db.session.commit()

    return jsonify({"message": f"Location '{location.name}' added to favorites"}), 201




#DELETE USERS POR ID
@api.route('/users/<int:id>', methods = ['DELETE'])
def delete_user (id):
    user = User.query.get(id)

    if user is None: 
        return jsonify({"error": "User not found"}), 404
    
    #aqui se aplica el comando de borrado de alchemy
    db.session.delete(user)

    #hacemos el commit
    db.session.commit()
#se borró el usuario con id indicado en la URL con éxito.
    return jsonify ({"message": f"User {user.id} deleted"}), 200


# DELETE ELIMINAR PERSONAJES FAVORITOS
@api.route('/favorite/character/<int:character_id>', methods=['DELETE'])
def delete_favorites_character(character_id):
    data = request.get_json()
    user_id = data.get("user_id")


    user = User.query.get(user_id)
    character = Characters.query.get(character_id)

    if not user or not character:
        return jsonify({"error": "User or Character not found"}), 404


    if character in user.favorite_characters:
        user.favorite_characters.remove(character)
        db.session.commit()
        return jsonify({"message": "favorite character deleted"}), 200
    else:
        return jsonify({"error": "Character not in favorites"}), 400

# DELETE Eliminar lugares favoritos
@api.route('/favorite/location/<int:location_id>', methods=['DELETE'])
def delete_favorites_location(location_id):
    data = request.get_json()
    user_id = data.get("user_id")


    user = User.query.get(user_id)
    location = Location.query.get(location_id)

    if not user or not location:
        return jsonify({"error": "User or Location not found"}), 404


    if location in user.favorite_locations:
        user.favorite_locations.remove(location)
        db.session.commit()
        return jsonify({"message": "favorite location deleted"}), 200
    else:
        return jsonify({"error": "Location not in favorites"}), 400




# >>>>>>>>>> PARA LAS PRUEBAS <<<<<<<<<<<<
# para probar en postman... POST
# {
#     "name": "Eliorcito",
#     "email": "Elior_21@gmail.com",
#     "password": 1345689
# }