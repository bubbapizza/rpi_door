#!/usr/bin/python
#
#        Copyright (C) 2013 Randy Topliffe
#        randytopliffe@gmail.com
#
#        
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

from unitcase import TestCase
from rpi_door.drivers import AbstractDoor
from rpi_door.models import init_db, drop_db, SQLAlchemyBinding


class BaseSuite(TestCase):

    def setUp(self):
        init_db()

    def tearDown(self):
        drop_db()


class TestDoor(AbstractDoor, SQLAlchemyBinding):

    def __init__(self, *args, **kwargs):
        super(TestDoor, self).__init__(*args, **kwargs)

    def check_for_lock_request(self):
        pass

    def read_RFID(self):
        pass

    def unlock(self):
        pass

    def lock(self):
        pass

    def toggle_red_led(self):
        pass

    def toggle_green_led(self):
        pass
