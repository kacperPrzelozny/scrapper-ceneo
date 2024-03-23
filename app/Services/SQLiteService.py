import sqlite3
from settings import ROOT_DIR


class SQLiteService:
    def getConnection(self):
        dbName = ROOT_DIR + '/data/ceneo_scrapper.db'
        conn = sqlite3.connect(dbName)
        c = conn.cursor()
        for query in open('data/init.sql').read().split(';'):
            c.execute(query)
        conn.commit()

        return conn
