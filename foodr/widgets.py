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
from simplekml import Kml, Style, IconStyle, Icon
from tropofy.widgets import KMLMap
from tropofy.app import Parameter, ParameterGroup

from .models import Person, Place


class FoodrParameterGroup(ParameterGroup):
    """
    Stores the parameters for the search (Needs to be open? and Radius to search)
    """
    OPEN = Parameter(name='open', label='Does the store need to be open?', default=True, allowed_type=bool)
    RADIUS = Parameter(name='radius', label='Search radius in meters?', default=5000, allowed_type=int)


class KMLMapInput(KMLMap):
    """
    Ripped from Tropofy docs basically.
    It's actually broken but it's not my fault, it should display the locations on a map.
    """
    def get_kml(self, app_session):

        kml = Kml()

        person_style = Style(iconstyle=IconStyle(scale=0.8, icon=Icon(
            href='https://maps.google.com/mapfiles/kml/paddle/blu-circle-lv.png')))
        people_folder = kml.newfolder(name="Potential Facilities")
        for p in [people_folder.newpoint(name=person.name, coords=[(person.longitude, person.latitude)]) for person in
                  app_session.data_set.query(Person).all()]:
            p.style = person_style

        place_style = Style(iconstyle=IconStyle(scale=0.4, icon=Icon(
            href='https://maps.google.com/mapfiles/kml/paddle/red-circle-lv.png')))
        places_folder = kml.newfolder(name="Places")
        for p in [places_folder.newpoint(name=place.name, coords=[(place.longitude, place.latitude)]) for place in
                  app_session.data_set.query(Place).all()]:
            p.style = place_style

        return kml.kml()
