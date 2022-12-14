import platform

import singlestoredb.clients.pymysqlsv as sv
from singlestoredb.connection import build_params

DBNAME_BASE = 'pymysqlsv__test_%s_%s_%s_%s_' % \
              (
                  *platform.python_version_tuple()[:2],
                  platform.system(), platform.machine(),
              )


def pytest_sessionstart() -> None:
    params = build_params()
    conn = sv.connect(  # type: ignore
        host=params['host'], user=params['user'],
        passwd=params['password'], port=params['port'],
    )
    cur = conn.cursor()
    cur.execute(f'CREATE DATABASE IF NOT EXISTS {DBNAME_BASE}1')
    cur.execute(f'CREATE DATABASE IF NOT EXISTS {DBNAME_BASE}2')
    conn.close()


def pytest_sessionfinish() -> None:
    params = build_params()
    conn = sv.connect(  # type: ignore
        host=params['host'], user=params['user'],
        passwd=params['password'], port=params['port'],
    )
    cur = conn.cursor()
    cur.execute(f'DROP DATABASE {DBNAME_BASE}1')
    cur.execute(f'DROP DATABASE {DBNAME_BASE}2')
    conn.close()
