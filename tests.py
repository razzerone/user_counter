import datetime
import sqlite3
import unittest
from urllib.parse import urlparse

from flask import Flask
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from SQLite_impl import SQLiteRepository
from app import app
from database.UserRepository_SqlAlchemy import UsersRepositoryImpl
from database.VisitsRepository_SqlAlchemy import VisitsRepositoryImpl
from database.tables import Base, engine
from smart_repo import SmartRepo
from user_counter import UserCounter


class SmarterRepoTest(unittest.TestCase):
    def setUp(self) -> None:
        self.rep = SmartRepo()

    def tearDown(self) -> None:
        self.rep.repo.drop_table()

    def testAdd(self):
        self.rep.add_new_user("1", "1", "1", "1")
        self.assertTrue(self.rep)

    def testCounterType(self):
        self.rep.add_new_user("1", "1", "1", "1")
        self.rep.repo.select()
        self.assertEqual(type(self.rep.get_users_count().get_id()), int)

    def testCounterValue(self):
        self.rep.add_new_user("1", "1", "1", "1")
        self.rep.repo.select()
        self.assertGreater(self.rep.get_users_count().get_id(), 0)

    def testOnLastVal(self):
        self.rep.add_new_user("1", "1", "1", "1")

        self.assertEqual((1, '1', '1', '1', '1'), self.rep.get_last()[:5])


class SqlTes(unittest.TestCase):
    def setUp(self) -> None:
        self.rep = SQLiteRepository('data.db')

    def testAdd(self):
        self.rep.add_new_user("192.168.0.1", "1", "1", "1")
        self.assertTrue(self.rep)

    def testCounter(self):
        self.rep.add_new_user("192.168.0.1", "1", "1", "1")
        self.assertEqual(1, self.rep.get_users_count()[0])

    def testCounterType(self):
        self.rep.add_new_user("192.168.0.1", "1", "1", "1")
        self.assertEqual(type(self.rep.get_users_count()[0]), int)

    def testOnLastVal(self):
        self.rep.add_new_user("192.168.0.1", "1", "1", "1")
        a = self.rep.get_last()
        self.assertEqual(1, a[0])
        self.assertEqual("192.168.0.1", a[2])
        self.assertEqual('1', a[3])
        self.assertEqual('1', a[4])
        self.assertEqual('1', a[5])

    def testGetAllUsers(self):
        self.rep.add_new_user("192.168.0.1", "1", "1", "1")
        self.rep.add_new_user("192.168.0.2", "1", "1", "1")
        self.rep.add_new_user("192.168.0.3", "1", "1", "1")

        r = self.rep.get_all_users()

        self.assertEqual(3, len(r))

    def testWrongIpFormat(self):
        with self.assertRaises(IOError):
            self.rep.add_new_user("1", "1", "1", "1")


class UserCounterTest(unittest.TestCase):
    def test_main(self):
        response = app.test_client().get('/')

        self.assertIsInstance(response.data, bytes)

    def test_reacheable(self):
        response = app.test_client().get('/')
        self.assertEqual(response.status_code, 200)

    def test_reacheable(self):
        response = app.test_client().get('/')
        self.assertEqual(response.status_code, 200)

    def test_suc_login_request(self):
        resp = app.test_client().post('/login', data=dict(username='111', password='111'), follow_redirects=True)
        self.assertIn('http://localhost/auth', str(resp.request))

    def test_bad_login_request(self):
        resp = app.test_client().post('/login', data=dict(username='123', password='123'), follow_redirects=True)

        self.assertIn('http://localhost/login', str(resp.request))

    def test_good_validate(self):
        resp = app.test_client().post('/validate_reg', data=dict(username='111', password='111'), follow_redirects=True)
        self.assertIn('User already exists', str(resp.data))

    def test_add_counter(self):
        resp1 = app.test_client().get('/count')
        app.test_client().post('/login', data=dict(username='111', password='111'), follow_redirects=True)
        resp2 = app.test_client().get('/count')

        self.assertNotEqual(resp1.data, resp2.data)

    def test_idempotency_counter(self):
        resp1 = app.test_client().get('/count')
        resp2 = app.test_client().get('/count')

        self.assertEqual(resp1.data, resp2.data)

    def test_last(self):
        resp1 = app.test_client().get('/last')
        app.test_client().post('/login', data=dict(username='111', password='111'), follow_redirects=True)
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
        app.test_client().post('/login', data=dict(username='111', password='111'), follow_redirects=True)
        resp2 = app.test_client().get('/all')
        self.assertNotEqual(resp1.data, resp2.data)

    def test_all_data_idempotency(self):
        resp1 = app.test_client().get('/all')
        resp2 = app.test_client().get('/all')
        self.assertEqual(resp1.data, resp2.data)


if __name__ == '__main__':
    unittest.main()
