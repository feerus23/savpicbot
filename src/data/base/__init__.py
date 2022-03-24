import sqlite3

con = sqlite3.connect(r"data\base\main.db")
cur = con.cursor()


def init():
    cur.execute('CREATE TABLE IF NOT EXISTS users (userid INT NOT NULL PRIMARY \
    KEY, channel_tag CHAR(32), language CHAR(63))')
    cur.execute('CREATE TABLE IF NOT EXISTS pictures (userid INT NOT NULL, \
    file_id VARCHAR(255) NOT NULL, keyword CHAR(65), \
    FOREIGN KEY (userid) REFERENCES userid (users))')
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
            self.__lan__ = None
            cur.execute(
                'INSERT INTO users (userid, language) VALUES (?, ?)', (userid,
                                                                       'rus'))
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
                cur.execute(
                    'INSERT INTO users (userid, channel_tag) VALUES (?, ?)',
                    (uid, value))
            else:
                cur.execute(
                    'UPDATE users SET channel_tag = ? WHERE userid = ?',
                    (value, uid))

            con.commit()

    def lang(self, value: str | None = None):
        uid = self.__uid__
        if value:
            cur.execute(
                'UPDATE users SET language = ? WHERE userid = ?', (value, uid))
            con.commit()
        else:
            return self.__lan__


class Picture:
    def __init__(self, user_id, keyword=None, file_id=None):
        self.__d = [user_id, keyword]
        if file_id:
            cur.execute('INSERT INTO pictures (userid, file_id, keyword) \
                    VALUES (?, ?, ?)', (user_id, file_id, keyword))
            con.commit()
        else:
            cur.execute('SELECT file_id FROM pictures WHERE userid = ? AND keyword = ?',
                        (user_id, keyword))
            self.__r = cur.fetchall()

    def get(self):
        return self.__r

    def set(self, file_id, keyword=None):
        kw = keyword if keyword else self.__d[1]
        user_id = self.__d[0]
        cur.execute('INSERT INTO pictures (userid, file_id, keyword) \
                VALUES (?, ?, ?)', (user_id, file_id, kw))
        con.commit()
