"""User View tests."""

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

class UserBaseViewTestCase(TestCase):
    def setUp(self):
        User.query.delete()

        u1 = User.signup("u1", "u1@email.com", "password", None)
        u2 = User.signup("u2", "u2@email.com", "password", None)
        
        db.session.add_all([u1, u2])
        db.session.commit()

        self.u1_id = u1.id
        self.u2_id = u2.id
      
        self.client = app.test_client()

    def tearDown(self):
        db.session.rollback()

class UserProfileTestCase(UserBaseViewTestCase):
    def test_user_profile_view(self):
        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.u1_id
            
            u1 = User.query.get(self.u1_id)
            resp = c.get(f"/users/{self.u1_id}")

            self.assertEqual(resp.status_code, 200)
            self.assertIn(u1.username, resp.text)


class UserWallTestCase(UserBaseViewTestCase):
    def test_users_view(self):
        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.u1_id

            u1 = User.query.get(self.u1_id)
            u2 = User.query.get(self.u2_id)

            resp = c.get(f"/users")

            self.assertEqual(resp.status_code, 200)
            self.assertIn(u1.username, resp.text)
            self.assertIn(u2.username, resp.text)
            


class UserFollowingViewTestCase(UserBaseViewTestCase):
    def test_users_following_view(self):
        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.u1_id

            u1 = User.query.get(self.u1_id)
            u2 = User.query.get(self.u2_id)

            u1.following.append(u2)

            db.session.commit()

            resp = c.get(f"/users/{self.u1_id}/following")

            self.assertEqual(resp.status_code, 200)
            self.assertIn(u2.username, resp.text)
    
    def test_users_followers_view(self):
        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.u1_id

            u1 = User.query.get(self.u1_id)
            u2 = User.query.get(self.u2_id)

            u1.following.append(u2)

            db.session.commit()

            resp = c.get(f"/users/{self.u2_id}/followers")

            self.assertEqual(resp.status_code, 200)
            self.assertIn(u1.username, resp.text)

    