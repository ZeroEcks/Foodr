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

from sqlalchemy.orm import relationship
from sqlalchemy.schema import Column, ForeignKeyConstraint, UniqueConstraint
from sqlalchemy.types import Text, Float, Integer
from tropofy.database.tropofy_orm import DataSetMixin


class Person(DataSetMixin):
    """
    Represents a persons location in the world
    """
    uuid = Column(Integer, nullable=False)
    name = Column(Text, nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)

    @classmethod
    def get_table_args(cls):
        return (UniqueConstraint('data_set_id', 'uuid'),)


class Place(DataSetMixin):
    """
    This represents a place which should basically be a food joint
    note: should be a unique joint, place_id must be unique.
    """
    uuid = Column(Integer, nullable=False)
    name = Column(Text, nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    value = Column(Integer, nullable=False)  # Nutritional Value
    place_id = Column(Text, nullable=False)  # GMaps stuff

    path = relationship('Path', cascade='all')

    @classmethod
    def get_table_args(cls):
        return (
            UniqueConstraint('data_set_id', 'uuid'),
            UniqueConstraint('data_set_id', 'place_id'),
        )


class Path(DataSetMixin):
    """
    A bit of an unholy mashup of the data required for finding the best option
    and data that needs to be displayed to the user.
    """
    uuid = Column(Integer, nullable=False)
    person_id = Column(Text, nullable=False)
    place_id = Column(Text, nullable=False)
    time = Column(Float, nullable=False)

    person = relationship(Person, viewonly=True)
    place = relationship(Place, viewonly=True)

    # Data for user display
    person_name = Column(Text, nullable=True)
    place_name = Column(Text, nullable=True)
    place_addr = Column(Text, nullable=True)

    @classmethod
    def get_table_args(cls):
        return (
            ForeignKeyConstraint(['person_id', 'data_set_id'],
                                 ['person.uuid', 'person.data_set_id'],
                                 ondelete='CASCADE', onupdate='CASCADE'),
            ForeignKeyConstraint(['place_id', 'data_set_id'],
                                 ['place.uuid', 'place.data_set_id'],
                                 ondelete='CASCADE', onupdate='CASCADE')
        )
