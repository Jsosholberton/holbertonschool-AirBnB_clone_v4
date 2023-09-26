#!/usr/bin/python3
'''
MODULE NAME:
------------
    100-hbnb

MODULE DESCRIPTION:
-------------------
    That return a HTML with the states, cities and amenities

MODULE ATTRUBUTES:
------------------
    None

ROUTES:
-------
    '/hbnb' Return a HTML
'''
import uuid
from flask import Flask, render_template
from models import storage
from models.state import State
from models.amenity import Amenity
from models.place import Place
from models.city import City

dict_instances = {"State": State, "Amenity": Amenity,
                  "Place": Place,"City": City}

app = Flask(__name__)
@app.route('/hbnb/<pag>', strict_slashes=False)
@app.route('/hbnb/<pag>/<inst>/<id>/', strict_slashes=False)
@app.route('/0-hbnb/', strict_slashes=False)
def state_list(inst=None, id=None, pag=1):
    places = storage.all(Place)
    states = storage.all(State)
    amenities = storage.all(Amenity)
    cities = storage.all(City)
    filter_inst = None

    if inst == 'State' and id:
        filter_inst = states["State." + id]
        if filter_inst:
            places = {key: place for key, place in places.items()\
                      if place.cities.state_id == id}
    elif inst == 'City' and id:
        filter_inst = cities["City." + id]
        if filter_inst:
            places = {key: place for key, place in places.items()\
                      if place.city_id == id}
    elif inst == "Amenity":
        filter_inst = amenities["Amenity." + id]
        if filter_inst:
            places = {key: place for key, place in places.items()\
                      if any(amenity.id == id for amenity in place.amenities)}

    pag = int(pag)

    if pag == 0:
        pag = 1

    last = pag * 4
    firts = last - 4

    if len(places) > 4:
        last = pag * 4
        sorted_items = sorted(places.items(), key=lambda x: x[1].name)
        places = dict(sorted_items[firts:last])

    return render_template('0-hbnb.html',
                           states=states,
                           amenities=amenities,
                           places=places,
                           filter=filter_inst,
                           pag=pag, cache_id = uuid.uuid4())


@app.teardown_appcontext
def teardown_db(*args, **kwargs):
    storage.close()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
