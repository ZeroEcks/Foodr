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
from tropofy import main as tropofy_main, serve_app_cascade

APP_CONFIG = {
    'tropofy': {
        'api_url': 'https://api.tropofy.com',
        'auth_url': 'https://auth.tropofy.com',
    },
    'database': {
        'url': 'sqlite:///foodr.db',
    },
    'apps': [
        {
            'module': 'foodr',
            'classname': 'FoodrApp',
            'config': {
                'key.public': '',
                'key.private': ''
            }
        }
    ]
}

APP = tropofy_main(APP_CONFIG)

if __name__ == "__main__":
    serve_app_cascade(APP, '0.0.0.0', 8080)
