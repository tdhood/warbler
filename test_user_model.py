"""User model tests."""

# run these tests like:
#
#    python -m unittest test_user_model.py


import os
from unittest import TestCase

from models import db, User, Message, Follows
from sqlalchemy.exc import DataError

# BEFORE we import our app, let's set an environmental variable
# to use a different database for tests (we need to do this
# before we import our app, since that will have already
# connected to the database

os.environ["DATABASE_URL"] = "postgresql:///warbler_test"

# Now we can import app

from app import app

# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data

db.create_all()


class UserModelTestCase(TestCase):
    def setUp(self):
        User.query.delete()

        u1 = User.signup("u1", "u1@email.com", "password", None)
        u2 = User.signup("u2", "u2@email.com", "password", None)

        db.session.commit()
        self.u1_id = u1.id
        self.u2_id = u2.id

        self.client = app.test_client()

    def tearDown(self):
        db.session.rollback()

    def test_user_model(self):
        u1 = User.query.get(self.u1_id)

        # User should have no messages & no followers
        self.assertEqual(len(u1.messages), 0)
        self.assertEqual(len(u1.followers), 0)

    def test_user_following(self):
        u1 = User.query.get(self.u1_id)
        u2 = User.query.get(self.u2_id)

        u1.following.append(u2)

        db.session.commit()

        # User should have no messages & no followers
        self.assertEqual(u2.following, [])
        self.assertEqual(u2.followers, [u1])
        self.assertEqual(u1.followers, [])
        self.assertEqual(u1.following, [u2])

    def test_user_repr(self):
        u1 = User.query.get(self.u1_id)
        result = repr(u1)
        self.assertEqual(result, f"<User #{self.u1_id}: u1, u1@email.com>")

    def test_user_signup(self):
        u3 = User.signup("u3", "u3@email.com", "password", None)

        self.assertIsInstance(u3, User)
        self.assertEqual(u3.username, "u3")
        self.assertNotEqual(u3.password, "password")
    
    
    def test_user_authenticate(self):
        u1 = User.query.get(self.u1_id)
        result = u1.authenticate("u1", "password")

        self.assertIsInstance(result, User)

    def test_user_invalid_authenticate(self):
        u1 = User.query.get(self.u1_id)
        result = u1.authenticate("u5", "password")
        result2 = u1.authenticate("u1", "badpassword")

        self.assertEqual(result, False)
        self.assertEqual(result2, False)





    
      
       
