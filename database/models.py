# Copyright (C) 2013 Windsor Hackforge
#
# This module is part of RPi Door and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php

class SQLAlchemyMixin(SQLAlchemyBase):
   """This class adds special functions to the SQL database."""

    def validate_key_code(self, data):
        key = KeyCode.query\
                     .options(joinedload(KeyCode.user))\
                     .filter(KeyCode.code == data)\
                     .first()

        if key and (key.user and key.enabled):
            return True
        return False

    def create_user(self, data):
        with self.session_context() as session:
            user = User(**data)
            session.add(user)
            session.commit()
