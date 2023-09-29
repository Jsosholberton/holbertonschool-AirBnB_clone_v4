#!/usr/bin/python3

""" This view Handles all restful API actions for State"""

from api.v1.views import app_views
from flask import request, jsonify, abort
from models import storage
from models.city import City
from models.user import User
from models.place import Place
from models.state import State
from models.amenity import Amenity
from models.review import Review

# Define la función my_dict para convertir objetos Place en diccionarios
def my_dict(self, **kwargs):
    """Convert the object to a dictionary."""
    return {
        "id": self.id,
        "city_id": self.city_id,
        "user_id": self.user_id,
        "name": self.name,
        "description": self.description,
        "number_rooms": self.number_rooms,
        "number_bathrooms": self.number_bathrooms,
        "max_guest": self.max_guest,
        "price_by_night": self.price_by_night,
        "latitude": self.latitude,
        "longitude": self.longitude,
        "user": storage.get(User, self.user_id).to_dict()
    }

Place.to_dict = my_dict


@app_views.route('cities/<city_id>/places',
                 methods=['GET', 'POST'], strict_slashes=False)
def places_by_city(city_id):
    """retrieve places based on city_id"""
    city = storage.get(City, city_id)
    if request.method == 'GET':
        if city:
            places = [place.to_dict() for place in city.places]
            return jsonify(places)
        abort(404)
    elif request.method == 'POST':
        if city is None:
            abort(404)
        request_data = request.get_json()
        if request_data is None:
            abort(400, 'Not a JSON')

        if "user_id" not in request_data:
            abort(400, "Missing user_id")

        user = storage.get(User, request_data["user_id"])
        if user is None:
            abort(404)
        if "name" not in request_data:
            abort(400, "Missing name")

        request_data['city_id'] = city_id
        new_place = Place(**request_data)
        new_place.save()

        return jsonify(new_place.to_dict()), 201


@app_views.route('/places/<string:place_id>',
                 methods=['GET', 'PUT', 'DELETE'], strict_slashes=False)
def place_by_place_id(place_id):
    """Retrieves a place based on the place_id"""
    place = storage.get(Place, place_id)

    if place is None:
        abort(404)
    if request.method == 'GET':
        return jsonify(place.to_dict())
    if request.method == 'DELETE':
        place.delete()
        storage.save()
        return jsonify({}), 200
    if request.method == 'PUT':
        my_dict = request.get_json()
        if my_dict is None:
            abort(400, 'Not a JSON')
        for k, v in my_dict.items():
            if k not in ("id", "user_id", "city_id",
                         "created_id", "updated_id"):
                setattr(place, k, v)
        place.save()
        return jsonify(place.to_dict()), 200

@app_views.route('/places_search',
                 methods=['POST'], strict_slashes=False)
def places_search():

    list_places = []
    list_amenities = []

    request_data = request.get_json()
    if request_data is None:
        abort(400, 'Not a JSON')

    try:
        if request_data['amenities']:
            list_amenities = [amty for amty in request_data['amenities']]

    except Exception:
        pass

    try:
        if request_data["states"] and request_data["cities"]:
            for state in request_data["states"]:
                new_state = storage.get(State, state)
                for city in new_state.cities:
                    for place in city.places:
                        list_places.append(place.to_dict())

            for id in request_data["cities"]:
                new_city = storage.get(City, id)
                for place in new_city.places:
                    if place not in list_places:
                        list_places.append(place.to_dict())
    except Exception:
        pass

    try:
        if request_data["states"]:
            for state in request_data["states"]:
                new_state = storage.get(State, state)
                for city in new_state.cities:
                    for place in city.places:
                        place_final = place.to_dict()
                        if list_amenities:
                            for amty in place.amenities:
                                if amty.id in list_amenities:
                                    list_places.append(place_final)
                        else:
                            list_places.append(place.to_dict())
            return jsonify(list_places)
    except Exception:
        pass

    try:
        if request_data["cities"]:
            for id in request_data["cities"]:
                new_city = storage.get(City, id)
                for place in new_city.places:
                    place_final = place.to_dict()
                    if list_amenities:
                        for amty in place.amenities:
                            if amty.id in list_amenities:
                                list_places.append(place_final)
                    else:
                        list_places.append(place.to_dict())
        return jsonify(list_places)
    except Exception:
        pass

    if list_amenities:
        places = storage.all(Place).values()
        filtered_places = []
        for place in places:
            place_amenities = {amty.id for amty in place.amenities}
            if set(list_amenities).issubset(place_amenities):
                filtered_places.append(place.to_dict())
        return filtered_places

    places = storage.all(Place).values()
    list_places = [place.to_dict() for place in places]

    return list_places
