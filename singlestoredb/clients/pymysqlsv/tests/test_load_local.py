# type: ignore
import os

from singlestoredb.clients.pymysqlsv import cursors
from singlestoredb.clients.pymysqlsv import OperationalError
from singlestoredb.clients.pymysqlsv import Warning
from singlestoredb.clients.pymysqlsv.tests import base

__all__ = ['TestLoadLocal']


class TestLoadLocal(base.PyMySQLTestCase):
    def test_no_file(self):
        """Test load local infile when the file does not exist"""
        conn = self.connect()
        c = conn.cursor()
        c.execute('CREATE TABLE test_load_local (a INTEGER, b INTEGER, c TEXT)')
        try:
            self.assertRaises(
                OperationalError,
                c.execute,
                (
                    "LOAD DATA LOCAL INFILE 'no_data.txt' INTO TABLE "
                    "test_load_local fields terminated by ','"
                ),
            )
        finally:
            c.execute('DROP TABLE test_load_local')
            c.close()

    def test_load_file(self):
        """Test load local infile with a valid file"""
        conn = self.connect()
        c = conn.cursor()
        c.execute('CREATE TABLE test_load_local (a INTEGER, b INTEGER, c TEXT)')
        filename = os.path.join(
            os.path.dirname(os.path.realpath(__file__)), 'data', 'load_local_data.txt',
        )
        try:
            c.execute(
                f"LOAD DATA LOCAL INFILE '{filename}' INTO TABLE test_load_local FIELDS TERMINATED BY ','",
            )
            c.execute('SELECT COUNT(*) FROM test_load_local')
            self.assertEqual(22749, c.fetchone()[0])
        finally:
            c.execute('DROP TABLE test_load_local')

    def test_unbuffered_load_file(self):
        """Test unbuffered load local infile with a valid file"""
        conn = self.connect(cursorclass=cursors.SSCursor)
        c = conn.cursor()
        c.execute('CREATE TABLE test_load_local (a INTEGER, b INTEGER, c TEXT)')
        filename = os.path.join(
            os.path.dirname(os.path.realpath(__file__)), 'data', 'load_local_data.txt',
        )
        try:
            c.execute(
                f"LOAD DATA LOCAL INFILE '{filename}' INTO TABLE test_load_local FIELDS TERMINATED BY ','",
            )
            c.execute('SELECT COUNT(*) FROM test_load_local')
            self.assertEqual(22749, c.fetchone()[0])
        finally:
            c.close()
            conn.close()
            conn.connect()
            c = conn.cursor()
            c.execute('DROP TABLE test_load_local')


if __name__ == '__main__':
    import unittest

    unittest.main()
