"""
Author: Melody Kelly

This file is part of Foodr.

Foodr is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Foodr is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Foodr.  If not, see <http://www.gnu.org/licenses/>.
"""
import sys
import googlemaps

from datetime import datetime
from tropofy.widgets import ExecuteFunction

from .models import Place, Person, Path

# Create a global gmaps client so I don't have to reinitialize it all the time.
# Just moved this to a file, normally I would probably have a big file of all the keys
# or I would use environment variables.
API_KEY = ''

with open("apikey", "r") as f:
    API_KEY = f.read()

gmaps = googlemaps.Client(key=API_KEY)


class FindNearbyPlaces(ExecuteFunction):
    """
    Button for running the search for food
    """
    def get_button_text(self, app_session):
        return "Search for food"

    def execute_function(self, app_session):
        findNearbyFood(app_session)


def findNearbyFood(app_session):
    """
    Queries Google Maps for nearby fast food.
    """
    # I should probably pull this from the database
    JOINTS = [('Hungry Jacks', 4), ('TEAMASTER', 10), ('Govindas', 8)]

    app_session.task_manager.send_progress_message("Commencing search")

    People = app_session.data_set.query(Person).all()
    Places = []

    uuid = 1  # This UUID stuff is because i couldn't get autoincrement on the pk working properly.
    for person in People:
        person_loc = (person.latitude, person.longitude)
        for joint in JOINTS:
            # Using app_session.data_set.get_param seems to be kind of broken and doesn't return the default value so
            # I am just chucking in a or so there is one.
            # Also I can't just add an or for open_now because False is falsy and so is None so I have to check if None
            open_now = True if app_session.data_set.get_param('open') is None else app_session.data_set.get_param('open')
            radius = app_session.data_set.get_param('radius') or 5000
            search = gmaps.places_radar(location=person_loc, keyword=joint[0],
                                        open_now=open_now, radius=radius)
            # Comb through the results and remove duplicates
            for result in search['results']:
                # Check if any places have the same place_id already, if so, don't bother adding it.
                # This speeds things up a fair bit if the people are near each other.
                if any(x.place_id == result['place_id'] for x in Places):
                    continue
                details = gmaps.place(result['place_id']) # Google doesn't return any details unless you query again.
                place = Place(uuid=uuid,
                              place_id=result['place_id'],
                              name=details['result']['name'],
                              latitude=result['geometry']['location']['lat'],
                              longitude=result['geometry']['location']['lng'],
                              value=joint[1])
                Places.append(place)
                uuid = uuid + 1
            app_session.task_manager.send_progress_message('Processed a joint')
        app_session.task_manager.send_progress_message('Processed a person')
    app_session.data_set.add_all(Places)


class ExecuteSolverFunction(ExecuteFunction):
    """
    Button to execute the solving of optimal fast food
    """
    def get_button_text(self, app_session):
        return "Solve Food Location Problem"

    def execute_function(self, app_session):
        if len(app_session.data_set.query(Place).all()) > 200:
            app_session.task_manager.send_progress_message(
                "You can only solve problems with 200 shops of fewer using the free version of this app")
        else:
            formulate_and_solve_best_location_problem(app_session)


def formulate_and_solve_best_location_problem(app_session):
    """
    Compute the best location to a person.
    """
    # Send a progress message
    app_session.task_manager.send_progress_message("Commencing optimisation")

    People = app_session.data_set.query(Person).all()
    Places = app_session.data_set.query(Place).all()
    places_addr = []
    people_addr = []
    PeoplesRoutes = {}
    BestOption = {}

    # Send a progress message
    app_session.task_manager.send_progress_message("Computing the travel times")

    for person in People:
        person = gmaps.reverse_geocode((person.latitude, person.longitude))
        people_addr.append(person[0]['formatted_address'])
    for place in Places:
        places_addr.append(gmaps.place(place.place_id)['result']['formatted_address'])

    Places = zip(Places, places_addr)
    People = zip(People, people_addr)

    now = datetime.now()
    id = 1
    for person in People:
        PeoplesRoutes[person[1]] = []
        for place in Places:
            direction = gmaps.directions(person[1], place[1], mode="driving", departure_time=now)
            time = direction[0]['legs'][0]['duration']['value']  # duration in seconds
            path = Path(uuid=id, person_id=person[0].uuid, place_id=place[0].uuid, place_name=place[0].name,
                        place_addr=place[1], person_name=person[0].name, time=time)
            PeoplesRoutes[person[1]].append(path)
            id = id + 1

    for key, value in PeoplesRoutes.iteritems():
        best = sys.maxint
        for option in value:
            # This bit could be better, i could even grab it from the database stuff i already pulled, but also i found
            # it was easier to just use sqlalchemy in my head and I haven't revised this much.
            place_value = app_session.data_set.query(Place).filter(Place.uuid == option.place_id).first().value
            worth = option.time - (place_value * 100)
            if worth < best:
                BestOption[key] = option
                best = worth

    for key, value in BestOption.iteritems():
        app_session.data_set.add(value)

    app_session.task_manager.send_progress_message("Finished Optimising your routes :)")
