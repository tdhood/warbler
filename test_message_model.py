"""Message Model tests."""

# run these tests like:
#
#    FLASK_ENV=production python -m unittest test_message_views.py


import os
from unittest import TestCase

from models import db, Message, User

# BEFORE we import our app, let's set an environmental variable
# to use a different database for tests (we need to do this
# before we import our app, since that will have already
# connected to the database

os.environ['DATABASE_URL'] = "postgresql:///warbler_test"

# Now we can import app

from app import app, CURR_USER_KEY

app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data

db.create_all()

# Don't have WTForms use CSRF at all, since it's a pain to test

app.config['WTF_CSRF_ENABLED'] = False


class MessageModelTestCase(TestCase):
    def setUp(self):
        Message.query.delete()
        User.query.delete()

        u1 = User.signup("u1", "u1@email.com", "password", None)
        db.session.flush()

        m1 = Message(text="m1-text", user_id=u1.id)
        db.session.add_all([m1])
        db.session.commit()

        self.u1_id = u1.id
        self.m1_id = m1.id

        self.client = app.test_client()

    def tearDown(self):

        db.session.rollback()

    def test_message_user(self):
        message = Message.query.get(self.m1_id)
        u1 = User.query.get(self.u1_id)

        user = message.user

        self.assertEqual(user, u1)

    def test_message_likes(self):
        message = Message.query.get(self.m1_id)
        u1 = User.query.get(self.u1_id)
        u1.liked_messages.append(message)

        liked_messages = u1.liked_messages
        liked_by_users = message.liked_by_users

        self.assertEqual(liked_messages, [message])
        self.assertEqual(liked_by_users, [u1])