import sqlite3
import os

dbpath = os.getenv("DBURL")
con = sqlite3.connect(dbpath)
cur = con.cursor()


def init():
    cur.execute('CREATE TABLE IF NOT EXISTS users (userid INT NOT NULL PRIMARY KEY, channel_tag CHAR(32), \
    language CHAR(63))')
    con.commit()


class Users:
    def __init__(self, userid):
        cur.execute('SELECT * FROM users WHERE userid = ?', (userid,))
        row = cur.fetchone()

        if row:
            self.__uid__ = userid
            self.__tag__ = row[1]
            self.__lan__ = row[2]
        else:
            self.__uid__ = userid
            self.__lan__ = 'rus'
            cur.execute('INSERT INTO users (userid, language) VALUES (?, ?)', (userid, 'rus'))
            con.commit()

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
                cur.execute('INSERT INTO users (userid, channel_tag) VALUES (?, ?)', (uid, value))
            else:
                cur.execute('UPDATE users SET channel_tag = ? WHERE userid = ?', (value, uid))

            con.commit()

    def lang(self, value: str | None = None):
        uid = self.__uid__
        if value:
            cur.execute('UPDATE users SET language = ? WHERE userid = ?', (value, uid))
            con.commit()
        else:
            return self.__lan__
