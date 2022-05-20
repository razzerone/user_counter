import datetime
import sqlite3
import unittest

from SQLite_impl import SQLiteRepository
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
    def testGetIpCountry(self):
        self.assertEqual('US', UserCounter.get_ip_country('8.8.8.8'))


if __name__ == '__main__':
    unittest.main()
