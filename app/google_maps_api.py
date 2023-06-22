import os
import googlemaps
from project.entities.place import Place


def places_API(latitude, longitude, place_type, keyword):
    gmaps = googlemaps.Client(key=os.getenv('GOOGLE_API_KEY'))

    location = (latitude, longitude)

    places_result = gmaps.places_nearby(location=location, type=place_type, language='uk',
                                        open_now=True, rank_by='distance', keyword=keyword)
    places = []

    for place_result in places_result['results'][:5]:
        place_location = place_result['geometry']['location']
        places.append(Place(place_name=place_result['name'], place_address=place_result['vicinity'],
                            longitude=place_location['lng'], latitude=place_location['lat']))
    return places
