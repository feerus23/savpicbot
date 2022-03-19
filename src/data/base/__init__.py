import sqlite3
import os

dbpath = os.getenv("DBURL")
con = sqlite3.connect(dbpath)
cur = con.cursor()


def init():
    cur.execute('CREATE TABLE IF NOT EXISTS users (userid INT NOT NULL PRIMARY KEY, channeltag CHAR(32), \
    language CHAR(63) NOT NULL DEFAULT rus)')
    con.commit()


class Users:
    def __init__(self, userid):
        cur.execute('SELECT channeltag FROM users WHERE userid = ?', (userid,))
        row = cur.fetchone()

        if row:
            self.__uid__ = userid
            self.__tag__ = row[0]
            self.__lan__ = row[1]
        else:
            self.__uid__ = userid
            self.__lan__ = 'rus'

    def __call__(self, value: str | None = None):
        if not value:
            try:
                tag = self.__tag__
            except AttributeError:
                return None
            else:
                return tag
        else:
            uid = self.__uid__
            try:
                tag = self.__tag__
            except AttributeError:
                cur.execute('INSERT INTO users (userid, channeltag) VALUES (?, ?)', (uid, value))
            else:
                cur.execute('UPDATE users SET channeltag = ? WHERE userid = ?', (value, uid))

            con.commit()

    def lang(self):
        return self.__lan__
