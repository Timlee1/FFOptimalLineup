import os
os.environ['DATABASE_URL'] = 'sqlite://'

from datetime import datetime, timedelta
import unittest
from app import app, db
from app.models import User, League

class UserModelCase(unittest.TestCase):
    def setUp(self):
        self.app_context = app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_password_hashing(self):
        u = User(username='susan')
        u.set_password('cat')
        self.assertFalse(u.check_password('dog'))
        self.assertTrue(u.check_password('cat'))

    def test_user_league(self):
        # create four users
        u1 = User(username='john', email='john@example.com')
        u2 = User(username='susan', email='susan@example.com')
        u3 = User(username='mary', email='mary@example.com')
        u4 = User(username='david', email='david@example.com')
        db.session.add_all([u1, u2, u3, u4])

        # create four posts
        l1 = League(author=u1)
        l2 = League(author=u2)
        l3 = League(author=u3)
        l4 = League(author=u4)
        db.session.add_all([l1, l2, l3, l4])
        db.session.commit()

        # check the followed posts of each user
        f1 = u1.user_league().all()
        f2 = u2.user_league().all()
        f3 = u3.user_league().all()
        f4 = u4.user_league().all()
        self.assertEqual(f1, [l1])
        self.assertEqual(f2, [l2])
        self.assertEqual(f3, [l3])
        self.assertEqual(f4, [l4])

if __name__ == '__main__':
    unittest.main(verbosity=2)