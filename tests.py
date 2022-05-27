import unittest

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from werkzeug.security import generate_password_hash

import app as app_file

from app import app
from database import tables
from database.user_repository_sqlalchemy import UsersRepositoryImpl
from database.visit_repository_sqlalchemy import VisitsRepositoryImpl
from user_counter import UserCounter


class UserCounterTest(unittest.TestCase):
    def setUp(self):
        self.engine = create_engine('sqlite:///test.db', echo=True)

        app_file.visit_repo = VisitsRepositoryImpl(engine=self.engine)
        app_file.user_repo = UsersRepositoryImpl(engine=self.engine)
        app_file.user_counter = UserCounter(
            app_file.visit_repo,
            app_file.user_repo
        )

        tables.engine = self.engine
        tables.Base.metadata.create_all(self.engine)
        self.session_fabric = sessionmaker(bind=self.engine)

        with self.session_fabric() as s:
            if s.query(tables.DatabaseVisit).count() > 0:
                s.query(tables.DatabaseVisit).delete()
            if s.query(tables.DatabaseUser).count() > 0:
                s.query(tables.DatabaseUser).delete()

        with self.session_fabric() as s:
            s.add(tables.DatabaseUser(
                login='111',
                password_hash=generate_password_hash('111')
            ))
            s.commit()

    def tearDown(self):
        with self.session_fabric() as s:
            s.query(tables.DatabaseUser).delete()
            s.query(tables.DatabaseVisit).delete()
            s.commit()

    def test_main(self):
        response = app.test_client().get('/')

        self.assertIsInstance(response.data, bytes)

    def test_reachable(self):
        response = app.test_client().get('/')
        self.assertEqual(response.status_code, 200)

    def test_suc_login_request(self):
        resp = app.test_client().post(
            '/login',
            data=dict(username='111', password='111'),
            follow_redirects=True
        )
        self.assertIn('http://localhost/auth', str(resp.request))

    def test_bad_login_request(self):
        resp = app.test_client().post(
            '/login',
            data=dict(username='123', password='123'),
            follow_redirects=True
        )

        self.assertIn('http://localhost/login', str(resp.request))

    def test_good_validate(self):
        resp = app.test_client().post(
            '/validate_reg',
            data=dict(username='111', password='111'),
            follow_redirects=True
        )
        self.assertIn('User already exists', str(resp.data))

    def test_add_counter(self):
        resp1 = app.test_client().get('/count')
        app.test_client().post(
            '/login',
            data=dict(username='111', password='111'),
            follow_redirects=True
        )
        resp2 = app.test_client().get('/count')

        self.assertNotEqual(resp1.data, resp2.data)

    def test_idempotency_counter(self):
        resp1 = app.test_client().get('/count')
        resp2 = app.test_client().get('/count')

        self.assertEqual(resp1.data, resp2.data)

    def test_last(self):
        resp1 = app.test_client().get('/last')
        app.test_client().post(
            '/login',
            data=dict(username='111', password='111'),
            follow_redirects=True
        )
        resp2 = app.test_client().get('/last')
        self.assertNotEqual(resp1.data, resp2.data)

    def test_last_idempotency(self):
        resp1 = app.test_client().get('/last')
        resp2 = app.test_client().get('/last')
        self.assertEqual(resp1.data, resp2.data)

    def test_first_idempotency(self):
        resp1 = app.test_client().get('/first')
        resp2 = app.test_client().get('/first')
        self.assertEqual(resp1.data, resp2.data)

    def test_all_data_onAdd(self):
        resp1 = app.test_client().get('/all')
        app.test_client().post(
            '/login',
            data=dict(username='111', password='111'),
            follow_redirects=True
        )
        resp2 = app.test_client().get('/all')
        self.assertNotEqual(resp1.data, resp2.data)

    def test_all_data_idempotency(self):
        resp1 = app.test_client().get('/all')
        resp2 = app.test_client().get('/all')
        self.assertEqual(resp1.data, resp2.data)


if __name__ == '__main__':
    unittest.main()
