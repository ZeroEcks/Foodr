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
import pkg_resources

from tropofy.app import AppWithDataSets, Step, StepGroup
from tropofy.widgets import SimpleGrid, ParameterForm
from tropofy.file_io import read_write_xl

from .models import Person, Place, Path
from .widgets import KMLMapInput, FoodrParameterGroup
from .solver import ExecuteSolverFunction, FindNearbyPlaces


class FoodrApp(AppWithDataSets):
    """
    Main Tropofy Class

    Contains all the stuff I have to implement to make a useful program
    """

    def get_name(self):
        return "Foodr"

    def get_examples(self):
        return {"Brisbane Data": load_brisbane_data}

    def get_static_content_path(self, app_session):
        return pkg_resources.resource_filename('foodr', 'static')

    def get_parameters(self):
        return FoodrParameterGroup.get_params()

    def get_gui(self):
        step_options = StepGroup(name='Parameters')
        step_options.add_step(Step(
            name='Parameters',
            widgets=[ParameterForm()],
            help_text="Enter the parameters you want."
        ))
        step_group1 = StepGroup(name='Enter your data')
        step_group1.add_step(Step(
            name='Enter your people',
            widgets=[SimpleGrid(Person)],
            help_text="Enter the set of locations, of people who need food"
        ))
        step_group1.add_step(Step(
            name='Search for nearby food',
            widgets=[FindNearbyPlaces()],
            help_text="Search for nearby food joints that are open."
        ))
        step_group1.add_step(Step(
            name='Enter your locations',
            widgets=[SimpleGrid(Place)],
            help_text="Enter the set of places with their nutritional value."
        ))
        step_group1.add_step(Step(
            name='Review your data',
            widgets=[KMLMapInput()],
            help_text="Review the locations and places entered for correctness"
        ))

        step_group2 = StepGroup(name='Solve')
        step_group2.add_step(Step(name='Solve Food Optimisation Problem', widgets=[
            ExecuteSolverFunction()]))

        step_group3 = StepGroup(name='View the Solution')
        step_group3.add_step(Step(
            name='Download KML',
            widgets=[
                {"widget": SimpleGrid(Path, hidden_column_names=["uuid", "person_id", "place_id"]), "cols": 6}
            ],
            help_text="Enjoy your optimised lunch :)"
        ))

        return [step_options, step_group1, step_group2, step_group3]


def load_brisbane_data(app_session):
    """
    Loads the data out of `people_example_data.xlsx`
    """
    read_write_xl.ExcelReader.load_data_from_excel_file_on_disk(
        app_session,
        pkg_resources.resource_filename('foodr', 'people_example_data.xlsx')
    )
